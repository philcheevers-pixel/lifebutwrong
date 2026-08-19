<?php
/**
 * Michelangelo Truth Serum — audit proxy
 * Deploy next to truth.html on pinkhouse.tech (currently missing / 404).
 *
 * POST JSON: { "text": "..." }
 * Returns Anthropic-shaped { content:[{type,text}], text, truthserum } for the live UI.
 */
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    header('Access-Control-Allow-Methods: POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type');
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'POST required']);
    exit;
}

$raw = file_get_contents('php://input');
$body = json_decode($raw, true);
if (!is_array($body)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON']);
    exit;
}

$text = isset($body['text']) ? trim((string)$body['text']) : '';
if ($text === '') {
    http_response_code(400);
    echo json_encode(['error' => 'Missing text']);
    exit;
}

$python = getenv('TRUTHSERUM_PYTHON') ?: 'python3';
$engine = __DIR__ . '/cli.py';
if (!is_file($engine)) {
    http_response_code(500);
    echo json_encode(['error' => 'Truth Serum engine missing (cli.py)']);
    exit;
}

$tmp = tempnam(sys_get_temp_dir(), 'ts_');
file_put_contents($tmp, $text);

$cmd = escapeshellcmd($python) . ' ' . escapeshellarg($engine) . ' --json --no-llm ' . escapeshellarg($tmp);
if (getenv('ANTHROPIC_API_KEY')) {
    // Prefer hybrid when a key is present.
    $cmd = escapeshellcmd($python) . ' ' . escapeshellarg($engine) . ' --json ' . escapeshellarg($tmp);
}

$descriptors = [
    0 => ['pipe', 'r'],
    1 => ['pipe', 'w'],
    2 => ['pipe', 'w'],
];
$proc = proc_open($cmd, $descriptors, $pipes, __DIR__, null);
if (!is_resource($proc)) {
    @unlink($tmp);
    http_response_code(500);
    echo json_encode(['error' => 'Failed to start Truth Serum engine']);
    exit;
}
fclose($pipes[0]);
$stdout = stream_get_contents($pipes[1]);
$stderr = stream_get_contents($pipes[2]);
fclose($pipes[1]);
fclose($pipes[2]);
$code = proc_close($proc);
@unlink($tmp);

if ($code !== 0) {
    http_response_code(500);
    echo json_encode(['error' => 'Audit engine failed', 'detail' => substr($stderr, 0, 400)]);
    exit;
}

$decoded = json_decode($stdout, true);
if (!is_array($decoded)) {
    http_response_code(500);
    echo json_encode(['error' => 'Engine returned non-JSON', 'detail' => substr($stdout, 0, 400)]);
    exit;
}

echo json_encode($decoded);
