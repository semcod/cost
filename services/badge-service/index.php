<?php
/**
 * AI Cost Badge Service - Main Entry Point
 * 
 * Provides endpoints for generating AI cost badges
 */

require_once 'badge.php';

// Router
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

switch ($path) {
    case '/':
    case '/badge':
        handleApiRequest();
        break;
    case '/health':
        header('Content-Type: application/json');
        echo json_encode(['status' => 'ok', 'service' => 'ai-cost-badge']);
        break;
    default:
        http_response_code(404);
        header('Content-Type: application/json');
        echo json_encode(['error' => 'Not found']);
}
