<?php
/**
 * Michelangelo Truth Serum — Stripe PaymentIntent + coupon bypass
 * Deploy next to truth.html on pinkhouse.tech (currently missing / 404).
 *
 * POST JSON: { "coupon": "..." }
 * Coupon bypass (matches live UI): { coupon_valid:true, client_secret:"coupon_bypass" }
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
    $body = [];
}

$coupon = isset($body['coupon']) ? trim((string)$body['coupon']) : '';
$expected = getenv('TRUTHSERUM_COUPON') ?: 'TESTFREE';

if ($coupon !== '' && hash_equals($expected, $coupon)) {
    echo json_encode([
        'coupon_valid' => true,
        'client_secret' => 'coupon_bypass',
    ]);
    exit;
}

$secret = getenv('STRIPE_SECRET_KEY') ?: '';
if ($secret === '') {
    echo json_encode([
        'error' => 'Payments are not configured. Ask Pink House for a test coupon, or set STRIPE_SECRET_KEY.',
    ]);
    exit;
}

$currency = getenv('TRUTHSERUM_CURRENCY') ?: 'cad';
$postFields = http_build_query([
    'amount' => 200,
    'currency' => $currency,
    'automatic_payment_methods' => ['enabled' => 'true'],
    'description' => 'Michelangelo Truth Serum audit',
]);

$ch = curl_init('https://api.stripe.com/v1/payment_intents');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $postFields,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_USERPWD => $secret . ':',
    CURLOPT_HTTPHEADER => ['Content-Type: application/x-www-form-urlencoded'],
    CURLOPT_TIMEOUT => 30,
]);
$response = curl_exec($ch);
$status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
$err = curl_error($ch);
curl_close($ch);

if ($response === false) {
    http_response_code(500);
    echo json_encode(['error' => 'Stripe request failed: ' . $err]);
    exit;
}

$data = json_decode($response, true);
if ($status >= 400 || !is_array($data) || empty($data['client_secret'])) {
    http_response_code(400);
    $msg = is_array($data) && isset($data['error']['message'])
        ? $data['error']['message']
        : 'Payment setup failed';
    echo json_encode(['error' => $msg]);
    exit;
}

echo json_encode(['client_secret' => $data['client_secret']]);
