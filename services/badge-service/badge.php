<?php
/**
 * AI Cost Badge Generator Service
 * 
 * This is a standalone PHP service that can be run as a separate project.
 * It generates SVG badges for AI cost tracking based on repository analysis.
 * 
 * Usage:
 *   GET /badge.php?cost=12.34&model=claude-4&format=svg
 *   GET /badge.php?cost=12.34&model=claude-4&format=svg&color=auto
 *   GET /badge.php?repo=github.com/user/repo&format=svg
 * 
 * Or as a REST API:
 *   POST /api/generate
 *   {
 *       "cost": 12.34,
 *       "model": "claude-4",
 *       "commits": 42,
 *       "format": "svg"
 *   }
 */

header('Content-Type: image/svg+xml');
header('Cache-Control: no-cache');

/**
 * Generate SVG badge
 */
function generateBadge(array $data): string {
    $cost = $data['cost'] ?? 0;
    $model = $data['model'] ?? 'unknown';
    $commits = $data['commits'] ?? 0;
    $label = $data['label'] ?? 'AI Cost';
    
    // Auto-determine color based on cost
    $color = determineColor($cost);
    if (isset($data['color']) && $data['color'] !== 'auto') {
        $color = $data['color'];
    }
    
    // Format cost
    $value = '$' . number_format($cost, 2);
    if ($commits > 0) {
        $value .= ' · ' . $commits . ' commits';
    }
    
    // Badge dimensions
    $labelWidth = strlen($label) * 6 + 10;
    $valueWidth = strlen($value) * 6 + 20;
    $totalWidth = $labelWidth + $valueWidth;
    $height = 20;
    
    // SVG template
    $svg = <<<SVG
<svg xmlns="http://www.w3.org/2000/svg" width="{$totalWidth}" height="{$height}" viewBox="0 0 {$totalWidth} {$height}">
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:#555;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#333;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="grad2" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:{$color};stop-opacity:1" />
            <stop offset="100%" style="stop-color:{$color};stop-opacity:0.8" />
        </linearGradient>
    </defs>
    
    <!-- Background -->
    <rect x="0" y="0" width="{$labelWidth}" height="{$height}" fill="url(#grad1)"/>
    <rect x="{$labelWidth}" y="0" width="{$valueWidth}" height="{$height}" fill="url(#grad2)"/>
    
    <!-- Rounded corners -->
    <rect x="0" y="0" width="3" height="{$height}" rx="3" fill="#555"/>
    <rect x="{$labelWidth}" y="0" width="3" height="{$height}" fill="#555"/>
    <rect x="{$labelWidth}" y="0" width="3" height="{$height}" fill="{$color}"/>
    <rect x="" y="0" width="3" height="{$height}" rx="3" fill="{$color}"/>
    
    <!-- Text -->
    <text x="5" y="14" font-family="sans-serif" font-size="11" fill="white">{$label}</text>
    <text x="{$labelWidth}" y="14" font-family="sans-serif" font-size="11" fill="white" text-anchor="middle">{$value}</text>
    
    <!-- Tooltip -->
    <title>AI Cost: \${$cost} with {$model} · {$commits} AI commits</title>
</svg>
SVG;
    
    return $svg;
}

/**
 * Determine badge color based on cost
 */
function determineColor(float $cost): string {
    if ($cost < 1) return '#4c1';        // brightgreen
    if ($cost < 5) return '#97ca00';     // green
    if ($cost < 10) return '#dfb317';    // yellow
    if ($cost < 50) return '#fe7d37';    // orange
    return '#e05d44';                     // red
}

/**
 * Analyze git repository and calculate costs
 */
function analyzeRepository(string $repoPath): array {
    $result = [
        'cost' => 0,
        'commits' => 0,
        'model' => 'unknown',
        'error' => null
    ];
    
    if (!is_dir($repoPath . '/.git')) {
        $result['error'] = 'Not a git repository';
        return $result;
    }
    
    // Get all commits with [ai:] tag
    $cmd = "cd " . escapeshellarg($repoPath) . " && git log --all --format='%H|%s|%ad|%an' --date=short --grep='\[ai:'";
    $output = shell_exec($cmd);
    
    if (empty($output)) {
        $result['error'] = 'No AI commits found';
        return $result;
    }
    
    $lines = explode("\n", trim($output));
    $result['commits'] = count($lines);
    
    // Calculate cost based on commit stats
    $totalCost = 0;
    foreach ($lines as $line) {
        $parts = explode('|', $line);
        if (count($parts) >= 2) {
            // Get diff size
            $hash = $parts[0];
            $diffCmd = "cd " . escapeshellarg($repoPath) . " && git show " . escapeshellarg($hash) . " --stat | tail -1";
            $diffOutput = shell_exec($diffCmd);
            
            // Parse lines changed
            if (preg_match('/(\d+)\s+insertions?.*?/', $diffOutput, $matches)) {
                $linesChanged = (int)$matches[1];
                // Rough estimation: 1000 lines = ~$0.50
                $cost = ($linesChanged / 1000) * 0.50;
                $totalCost += $cost;
            }
            
            // Extract model from commit message
            if (preg_match('/\[ai:([^\]]+)\]/', $parts[1], $modelMatch)) {
                $result['model'] = $modelMatch[1];
            }
        }
    }
    
    $result['cost'] = $totalCost;
    return $result;
}

/**
 * API endpoint handler
 */
function handleApiRequest(): void {
    $method = $_SERVER['REQUEST_METHOD'];
    
    if ($method === 'POST') {
        $input = json_decode(file_get_contents('php://input'), true);
        if (!$input) {
            http_response_code(400);
            echo json_encode(['error' => 'Invalid JSON']);
            return;
        }
        
        $svg = generateBadge($input);
        
        if (isset($input['format']) && $input['format'] === 'json') {
            header('Content-Type: application/json');
            echo json_encode([
                'svg' => $svg,
                'url' => 'data:image/svg+xml;base64,' . base64_encode($svg)
            ]);
        } else {
            header('Content-Type: image/svg+xml');
            echo $svg;
        }
        
    } else if ($method === 'GET') {
        $repo = $_GET['repo'] ?? null;
        
        if ($repo) {
            // Analyze repository
            $tempDir = sys_get_temp_dir() . '/ai-cost-' . uniqid();
            mkdir($tempDir);
            
            $cloneCmd = "git clone --depth 100 " . escapeshellarg("https://github.com/" . $repo . ".git") . " " . escapeshellarg($tempDir) . " 2>&1";
            shell_exec($cloneCmd);
            
            $data = analyzeRepository($tempDir);
            
            // Cleanup
            shell_exec("rm -rf " . escapeshellarg($tempDir));
            
            if ($data['error']) {
                http_response_code(404);
                echo generateBadge([
                    'cost' => 0,
                    'label' => 'AI Cost',
                    'commits' => 0,
                    'color' => '#9f9f9f'
                ]);
                return;
            }
            
            header('Content-Type: image/svg+xml');
            echo generateBadge($data);
            
        } else {
            // Generate from parameters
            $data = [
                'cost' => (float)($_GET['cost'] ?? 0),
                'model' => $_GET['model'] ?? 'unknown',
                'commits' => (int)($_GET['commits'] ?? 0),
                'label' => $_GET['label'] ?? 'AI Cost',
                'color' => $_GET['color'] ?? 'auto'
            ];
            
            header('Content-Type: image/svg+xml');
            echo generateBadge($data);
        }
    }
}

// Main entry point
handleApiRequest();
