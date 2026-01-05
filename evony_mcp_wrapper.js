/**
 * Node.js wrapper for Evony MCP Server
 * Keeps stdin pipe open and forwards to Python cleanly
 */
const { spawn } = require('child_process');
const path = require('path');
const readline = require('readline');

const pythonDir = 'c:\\Users\\Admin\\Downloads\\Evony_Decrypted';
const python = spawn('python', ['-m', 'evony_rag.mcp_server_clean'], {
    cwd: pythonDir,
    stdio: ['pipe', 'pipe', 'ignore']  // IGNORE stderr completely
});

// Forward stdout from Python to our stdout
python.stdout.on('data', (data) => {
    process.stdout.write(data);
});

// Read stdin line by line and forward to Python
const rl = readline.createInterface({
    input: process.stdin,
    terminal: false
});

rl.on('line', (line) => {
    python.stdin.write(line + '\n');
});

// Handle close
rl.on('close', () => {
    python.stdin.end();
});

python.on('exit', (code) => {
    process.exit(code || 0);
});

// Keep process alive
process.stdin.resume();
