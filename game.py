
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NEON DINO | Last Run</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    min-height: 100vh;
    background: #050611;
    color: white;
    font-family: Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
}

.game-container {
    width: min(1100px, 96%);
    position: relative;
    padding: 25px 0;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    gap: 12px;
}

.logo {
    font-size: clamp(22px, 4vw, 34px);
    font-weight: 900;
    letter-spacing: 5px;
}

.logo span {
    color: #ff743d;
    text-shadow: 0 0 18px #ff542b;
}

.subtitle {
    color: #7f91b8;
    font-size: 10px;
    letter-spacing: 4px;
    margin-top: 7px;
}

.status {
    color: #71ffd4;
    border: 1px solid #245b58;
    background: #0b2429;
    padding: 9px 13px;
    border-radius: 4px;
    font-size: 11px;
    letter-spacing: 2px;
    white-space: nowrap;
}

.game-window {
    position: relative;
    border: 1px solid #343453;
    border-radius: 10px;
    overflow: hidden;
    background: #080a20;
    box-shadow: 0 0 45px #171a4650,
                0 0 100px #ff573b0b;
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    aspect-ratio: 1000 / 430;
    cursor: crosshair;
}

.hud {
    position: absolute;
    top: 18px;
    left: 20px;
    right: 20px;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
}

.hud-label {
    color: #9aa8ce;
    font-size: 10px;
    letter-spacing: 3px;
}

.hud-value {
    font-size: 24px;
    font-weight: bold;
    margin-top: 5px;
    text-shadow: 0 0 15px #ff7545;
}

.hud-right {
    text-align: right;
}

.overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(
        90deg, #070817bb, #07081755, #070817bb
    );
    transition: opacity .3s;
}

.overlay.hidden {
    opacity: 0;
    pointer-events: none;
}

.overlay-content {
    padding: 20px;
}

.eyebrow {
    color: #ff8a57;
    font-size: 11px;
    letter-spacing: 5px;
    margin-bottom: 15px;
}

h1 {
    font-size: clamp(35px, 7vw, 70px);
    letter-spacing: 5px;
    line-height: 1;
    text-shadow: 0 0 35px #ff653b55;
}

h1 span {
    color: #ff7545;
}

.description {
    margin: 18px 0 25px;
    color: #b7bfdc;
    font-size: 13px;
    line-height: 1.8;
}

button {
    background: linear-gradient(110deg, #ff573b, #ff994d);
    border: none;
    border-radius: 4px;
    color: #130b13;
    padding: 15px 32px;
    font-weight: 900;
    letter-spacing: 3px;
    cursor: pointer;
    box-shadow: 0 0 30px #ff593b40;
    transition: transform .2s, box-shadow .2s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 40px #ff593b80;
}

.controls {
    display: flex;
    justify-content: center;
    gap: 25px;
    flex-wrap: wrap;
    margin: 20px 0;
    color: #a3adcb;
    font-size: 12px;
}

kbd {
    border: 1px solid #454766;
    background: #14172c;
    border-radius: 4px;
    padding: 5px 8px;
    color: white;
    margin-right: 5px;
}

.footer {
    border-top: 1px solid #22243b;
    padding-top: 16px;
    display: flex;
    justify-content: space-between;
    gap: 10px;
    color: #697493;
    font-size: 10px;
    letter-spacing: 2px;
}

@media (max-width: 600px) {
    .status { font-size: 9px; padding: 7px; }
    .subtitle { letter-spacing: 2px; }
    .hud { top: 10px; left: 12px; right: 12px; }
    .hud-value { font-size: 17px; }
    .hud-label { font-size: 8px; }
    .controls { gap: 12px; font-size: 10px; }
    .description { font-size: 11px; margin: 12px 0 17px; }
    button { padding: 12px 20px; font-size: 11px; }
}
</style>
</head>

<body>
<div class="game-container">

    <header class="topbar">
        <div>
            <div class="logo">NEON <span>DINO</span></div>
            <div class="subtitle">SURVIVE THE LAST RUN</div>
        </div>
        <div class="status">● SYSTEM ONLINE</div>
    </header>

    <main class="game-window">
        <canvas id="game" width="1000" height="430"></canvas>

        <div class="hud">
            <div>
                <div class="hud-label">DISTANCE</div>
                <div class="hud-value" id="score">00000</div>
            </div>
            <div class="hud-right">
                <div class="hud-label">PERSONAL BEST</div>
                <div class="hud-value" id="best">00000</div>
            </div>
        </div>

        <div class="overlay" id="overlay">
            <div class="overlay-content">
                <div class="eyebrow" id="eyebrow">MISSION 001 / ENDLESS</div>
                <h1 id="title">LAST <span>RUN</span></h1>
                <p class="description" id="description">
                    The world has gone dark.<br>
                    Keep running. Never look back.
                </p>
                <button id="start">INITIATE RUN</button>
            </div>
        </div>
    </main>

    <div class="controls">
        <span><kbd>SPACE</kbd><kbd>↑</kbd> JUMP</span>
        <span><kbd>↓</kbd> DUCK</span>
        <span><kbd>R</kbd> RESTART</span>
    </div>

    <footer class="footer">
        <span>NEON DINO // V.01</span>
        <span>NO SAVE POINTS. JUST SURVIVE.</span>
    </footer>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const scoreEl = document.getElementById("score");
const bestEl = document.getElementById("best");
const overlay = document.getElementById("overlay");
const startBtn = document.getElementById("start");

let best = Number(localStorage.getItem("neonDinoBest") || 0);
let score = 0;
let speed = 6;
let running = false;
let started = false;
let gameOver = false;
let frame = 0;
let distance = 0;
let spawnTimer = 70;
let obstacles = [];
let particles = [];
let stars = [];
let lastTime = 0;
let animationId;

const groundY = 350;

const dino = {
    x: 120,
    y: groundY - 55,
    w: 48,
    h: 55,
    vy: 0,
    grounded: true,
    ducking: false
};

bestEl.textContent = String(best).padStart(5, "0");

for (let i = 0; i < 100; i++) {
    stars.push({
        x: Math.random() * 1000,
        y: Math.random() * 260,
        r: Math.random() * 1.5 + 0.3,
        a: Math.random()
    });
}

function roundedRect(x, y, w, h, r, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, r);
    ctx.fill();
}

function background() {
    const gradient = ctx.createLinearGradient(0, 0, 0, 430);
    gradient.addColorStop(0, "#080a22");
    gradient.addColorStop(0.55, "#30204b");
    gradient.addColorStop(1, "#e45443");

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 1000, 430);

    // Stars
    stars.forEach(s => {
        ctx.globalAlpha = 0.3 + Math.abs(Math.sin(frame * 0.02 + s.a)) * 0.6;
        ctx.fillStyle = "#dce5ff";
        ctx.fillRect(s.x, s.y, s.r, s.r);
    });
    ctx.globalAlpha = 1;

    // Cinematic sun
    const sunGlow = ctx.createRadialGradient(760, 205, 5, 760, 205, 150);
    sunGlow.addColorStop(0, "#ffb56c88");
    sunGlow.addColorStop(1, "#ff654000");
    ctx.fillStyle = sunGlow;
    ctx.fillRect(590, 35, 340, 300);

    ctx.fillStyle = "#ffb16b";
    ctx.beginPath();
    ctx.arc(760, 205, 48, 0, Math.PI * 2);
    ctx.fill();

    // Sun stripes
    ctx.save();
    ctx.beginPath();
    ctx.arc(760, 205, 47, 0, Math.PI * 2);
    ctx.clip();
    ctx.fillStyle = "#d95d53";
    for (let y = 205; y < 260; y += 9) {
        ctx.fillRect(700, y, 120, 3);
    }
    ctx.restore();

    // Distant mountains
    drawMountains(0.15, "#292443", 265, 110);
    drawMountains(0.35, "#191b38", 300, 140);
    drawMountains(0.65, "#10142d", 320, 90);

    // Ground
    ctx.fillStyle = "#080c1c";
    ctx.fillRect(0, groundY, 1000, 80);

    ctx.strokeStyle = "#ff704e";
    ctx.lineWidth = 2;
    ctx.shadowBlur = 15;
    ctx.shadowColor = "#ff573b";
    ctx.beginPath();
    ctx.moveTo(0, groundY);
    ctx.lineTo(1000, groundY);
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Moving ground marks
    ctx.strokeStyle = "#3a345b";
    ctx.lineWidth = 2;

    for (let i = 0; i < 30; i++) {
        let x = ((i * 70 - distance * 3) % 1100 + 1100) % 1100;
        ctx.beginPath();
        ctx.moveTo(x, groundY + 22);
        ctx.lineTo(x - 18, groundY + 22);
        ctx.stroke();
    }
}

function drawMountains(factor, color, base, height) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(0, groundY);

    for (let x = 0; x <= 1100; x += 65) {
        const shift = (distance * factor) % 65;
        const px = x - shift;
        const peak = base - (height * (0.3 + 0.7 *
            Math.abs(Math.sin(x * 0.017 + factor * 10))));
        ctx.lineTo(px, peak);
        ctx.lineTo(px + 32, base + 20);
    }

    ctx.lineTo(1000, groundY);
    ctx.closePath();
    ctx.fill();
}

function drawDino() {
    const x = dino.x;
    const y = dino.y;
    const w = dino.w;
    const h = dino.h;

    ctx.save();

    // Neon aura
    ctx.shadowColor = "#6af9e5";
    ctx.shadowBlur = 17;
    ctx.fillStyle = "#8dffe9";

    if (dino.ducking) {
        roundedRect(x, groundY - 32, 59, 25, 5, "#69ead8");
        roundedRect(x + 38, groundY - 45, 27, 22, 4, "#69ead8");

        ctx.fillStyle = "#080c1c";
        ctx.fillRect(x + 54, groundY - 37, 5, 5);

        ctx.shadowBlur = 0;
        ctx.fillStyle = "#b0fff2";
        ctx.fillRect(x + 8, groundY - 8, 12, 7);
        ctx.fillRect(x + 38, groundY - 8, 12, 7);
    } else {
        // Body
        roundedRect(x + 6, y + 18, 33, 32, 5, "#69ead8");

        // Head
        roundedRect(x + 26, y, 27, 27, 5, "#8dffe9");

        // Tail
        ctx.beginPath();
        ctx.moveTo(x + 8, y + 28);
        ctx.lineTo(x - 9, y + 15);
        ctx.lineTo(x + 1, y + 37);
        ctx.closePath();
        ctx.fill();

        // Eye
        ctx.shadowBlur = 0;
        ctx.fillStyle = "#08101f";
        ctx.fillRect(x + 43, y + 8, 5, 5);

        // Legs
        ctx.fillStyle = "#8dffe9";
        if (dino.grounded && running) {
            const step = Math.sin(frame * 0.4) * 9;
            ctx.fillRect(x + 10, y + 43, 10, 12 + step);
            ctx.fillRect(x + 28, y + 43, 10, 12 - step);
        } else {
            ctx.fillRect(x + 10, y + 43, 9, 12);
            ctx.fillRect(x + 29, y + 43, 9, 12);
        }
    }

    ctx.restore();
}

function drawObstacle(o) {
    ctx.save();
    ctx.shadowColor = o.type === "bird" ? "#ffbd6b" : "#ff654d";
    ctx.shadowBlur = 15;

    if (o.type === "bird") {
        const flap = Math.sin(frame * 0.3) * 9;
        ctx.fillStyle = "#ffc47a";
        ctx.fillRect(o.x + 7, o.y, 27, 9);
        ctx.fillRect(o.x + 24, o.y - 7 + flap, 18, 5);
        ctx.fillRect(o.x + 12, o.y + 5, 18, 5);
        ctx.fillRect(o.x + 31, o.y + 3, 8, 5);
    } else {
        ctx.fillStyle = "#ff694f";
        ctx.fillRect(o.x + 5, o.y, o.w - 10, o.h);

        // Cactus branches
        ctx.fillRect(o.x - 3, o.y + 13, 12, 8);
        ctx.fillRect(o.x - 3, o.y + 6, 7, 15);
        ctx.fillRect(o.x + o.w - 9, o.y + 22, 12, 8);
        ctx.fillRect(o.x + o.w - 5, o.y + 14, 7, 16);

        ctx.fillStyle = "#ffd0a1";
        ctx.fillRect(o.x + 10, o.y + 8, 2, o.h - 15);
    }

    ctx.restore();
}

function spawnObstacle() {
    const bird = score > 100 && Math.random() < 0.30;

    if (bird) {
        obstacles.push({
            type: "bird",
            x: 1030,
            y: groundY - 48 - Math.random() * 22,
            w: 45,
            h: 24
        });
    } else {
        const h = 32 + Math.random() * 25;
        const w = 22 + Math.random() * 13;
        obstacles.push({
            type: "cactus",
            x: 1030,
            y: groundY - h,
            w: w,
            h: h
        });
    }
}

function addParticles(x, y, count) {
    for (let i = 0; i < count; i++) {
        particles.push({
            x: x,
            y: y,
            vx: (Math.random() - 0.5) * 5,
            vy: (Math.random() - 1) * 4,
            life: 20 + Math.random() * 20,
            color: Math.random() > 0.5 ? "#ff7545" : "#72ffe1"
        });
    }
}

function drawParticles() {
    particles.forEach(p => {
        ctx.globalAlpha = Math.max(0, p.life / 40);
        ctx.fillStyle = p.color;
        ctx.fillRect(p.x, p.y, 3, 3);
        p.x += p.vx;
        p.y += p.vy;
        p.life--;
    });
    particles = particles.filter(p => p.life > 0);
    ctx.globalAlpha = 1;
}

function jump() {
    if (!running) return;

    if (dino.grounded) {
        dino.vy = -14;
        dino.grounded = false;
        addParticles(dino.x + 20, groundY, 8);
    }
}

function startGame() {
    score = 0;
    speed = 6;
    frame = 0;
    distance = 0;
    spawnTimer = 65;
    obstacles = [];
    particles = [];

    dino.y = groundY - dino.h;
    dino.vy = 0;
    dino.grounded = true;
    dino.ducking = false;

    running = true;
    started = true;
    gameOver = false;
    lastTime = performance.now();

    overlay.classList.add("hidden");
    scoreEl.textContent = "00000";

    cancelAnimationFrame(animationId);
    animationId = requestAnimationFrame(loop);
}

function endGame() {
    running = false;
    gameOver = true;

    addParticles(dino.x + 25, dino.y + 25, 25);

    if (score > best) {
        best = score;
        localStorage.setItem("neonDinoBest", best);
        bestEl.textContent = String(best).padStart(5, "0");
    }

    document.getElementById("eyebrow").textContent =
        "MISSION FAILED // " + String(score).padStart(5, "0");

    document.getElementById("title").innerHTML =
        'GAME <span>OVER</span>';

    document.getElementById("description").innerHTML =
        "The run has ended.<br>Every failure makes the next run stronger.";

    startBtn.textContent = "RUN AGAIN";
    overlay.classList.remove("hidden");
    render();
}

function update(dt) {
    frame += dt;
    distance += speed * dt;

    score = Math.floor(distance / 10);
    speed = Math.min(13, 6 + score / 500);

    scoreEl.textContent = String(score).padStart(5, "0");

    // Gravity
    dino.vy += 0.65 * dt;
    dino.y += dino.vy * dt;

    if (dino.y >= groundY - dino.h) {
        dino.y = groundY - dino.h;
        dino.vy = 0;
        dino.grounded = true;
    }

    // Spawn obstacles
    spawnTimer -= dt;
    if (spawnTimer <= 0) {
        spawnObstacle();
        spawnTimer = Math.max(38, 85 - speed * 3) +
                     Math.random() * 35;
    }

    obstacles.forEach(o => {
        o.x -= speed * dt;

        // Collision box
        const dx = dino.x + 8;
        const dy = dino.ducking ? groundY - 29 : dino.y + 5;
        const dw = dino.ducking ? 49 : 35;
        const dh = dino.ducking ? 23 : 45;

        const ox = o.x + 3;
        const oy = o.y + 3;
        const ow = o.w - 6;
        const oh = o.h - 6;

        if (
            dx < ox + ow &&
            dx + dw > ox &&
            dy < oy + oh &&
            dy + dh > oy
        ) {
            endGame();
        }
    });

    obstacles = obstacles.filter(o => o.x > -100);

    // Occasional running sparks
    if (dino.grounded && Math.random() < 0.15) {
        particles.push({
            x: dino.x + 10,
            y: groundY - 2,
            vx: -Math.random() * 3,
            vy: -Math.random() * 2,
            life: 12,
            color: "#ff8057"
        });
    }
}

function render() {
    background();

    // Atmospheric floor glow
    const glow = ctx.createLinearGradient(0, groundY, 0, 430);
    glow.addColorStop(0, "#ff60451a");
    glow.addColorStop(1, "#080c1c00");
    ctx.fillStyle = glow;
    ctx.fillRect(0, groundY, 1000, 80);

    obstacles.forEach(drawObstacle);
    drawDino();
    drawParticles();

    // Cinematic vignette
    const vignette = ctx.createRadialGradient(
        500, 210, 130, 500, 210, 600
    );
    vignette.addColorStop(0, "#00000000");
    vignette.addColorStop(1, "#03040b99");
    ctx.fillStyle = vignette;
    ctx.fillRect(0, 0, 1000, 430);
}

function loop(timestamp) {
    if (!running) return;

    const dt = Math.min((timestamp - lastTime) / 16.67, 2);
    lastTime = timestamp;

    update(dt);
    render();

    if (running) {
        animationId = requestAnimationFrame(loop);
    }
}

function setDuck(value) {
    if (!running) return;
    dino.ducking = value;

    if (value && dino.grounded) {
        dino.y = groundY - 32;
        dino.h = 32;
    } else {
        dino.h = 55;
        if (dino.grounded) dino.y = groundY - 55;
    }
}

document.addEventListener("keydown", e => {
    if (["Space", "ArrowUp", "ArrowDown"].includes(e.code)) {
        e.preventDefault();
    }

    if (e.repeat) return;

    if (e.code === "Space" || e.code === "ArrowUp") {
        if (!running) startGame();
        else jump();
    }

    if (e.code === "ArrowDown") {
        setDuck(true);
    }

    if (e.code === "KeyR") {
        startGame();
    }
});

document.addEventListener("keyup", e => {
    if (e.code === "ArrowDown") setDuck(false);
});

canvas.addEventListener("pointerdown", () => {
    if (!running) startGame();
    else jump();
});

startBtn.addEventListener("click", startGame);

// Draw the opening scene
render();

</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(debug=True)
