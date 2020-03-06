function mainGame() {
    var c = document.getElementById("breakout");
    var ctx = c.getContext("2d");

    var bgctx = document.getElementById("breakoutbg").getContext("2d");
    bgctx.beginPath();
    var bggrad = ctx.createLinearGradient(0, 0, 0, c.height);
    bggrad.addColorStop(0, "rgb(0, 0, 0)");
    bggrad.addColorStop(1, "rgb(0, 0, 50)");
    bgctx.fillStyle = bggrad;
    bgctx.rect(0, 0, c.width, c.height);
    bgctx.fill();
    bgctx.font = "10px Gugi";
    bgctx.fillStyle = '#FFFFFF';
    bgctx.textAlign = "left";
    bgctx.fillText("Powered By Turnitin", 6, c.height - 6);

    var score = 0;

    var difficulty = {
        hard: {
            speed_multiplier: 1.5
        },
        normal: {
            speed_multiplier: 1
        },
        easy: {
            speed_multiplier: 0.7
        },
    };

    var ball = {
        pos: {
            x: c.width / 2 - 200,
            y: c.height / 2 - 2,
        },
        vel: {
            x: 6 * difficulty[currDiff]['speed_multiplier'],
            y: 6 * difficulty[currDiff]['speed_multiplier'],
        },
        r: 10,
        rot: 0,
        velr: 0,
        render: function () {
            this.pos.x += this.vel.x;
            this.pos.y += this.vel.y;
            if (this.oob(c.width, this.pos.x, this.r)) {
                this.vel.x = -this.vel.x;
                this.pos.x += this.vel.x;
                this.pos.y -= this.vel.y;
            }
            if (this.oob(c.height, this.pos.y, this.r)) {
                if (this.pos.y > c.height - this.r) {
                    endGame();
                }
                this.vel.y = -this.vel.y;
                this.pos.y += this.vel.y;
                this.pos.x -= this.vel.x;
            }

            ctx.save();
            ctx.beginPath();
            var gradient = ctx.createRadialGradient(this.pos.x, this.pos.y, 2, this.pos.x, this.pos.y, 10);
            ctx.fillStyle = "rgb(255, 232, 102)";
            ctx.strokeStyle = "rgb(255, 232, 102)";
            ctx.setLineDash([5, 5]);
            ctx.lineWidth = 4;
            ctx.translate(this.pos.x, this.pos.y);
            ctx.rotate(this.rot * Math.PI);
            ctx.arc(0, 0, this.r, 0, 2 * Math.PI);
            if (this.vel.x > 0) {
                this.velr = 0.01;
            } else if (this.vel.x < 0) {
                this.velr = -0.01;
            } else {
                this.velr = 0;
            }
            this.rot += this.velr;
            ctx.fill();
            ctx.stroke();
            ctx.restore();

        },
        oob: function (max, curr, offset) {
            if (curr < offset || curr > (max - offset)) {
                return true;
            }
        },
        left: function () {
            return this.pos.x - this.r;
        },
        right: function () {
            return this.pos.x + this.r;
        },
        top: function () {
            return this.pos.y - this.r;
        },
        bottom: function () {
            return this.pos.y + this.r;
        },
    };

    var paddle = {
        pos: {
            x: c.width / 2 + 2,
            y: c.height - 40,
        },
        width: 80,
        height: 20,
        render: function () {
            ctx.beginPath();
            var gradient = ctx.createLinearGradient(this.pos.x, this.pos.y, this.pos.x, this.pos.y + this.height);
            gradient.addColorStop(0, "#999999");
            gradient.addColorStop(0.7, "#eeeeee");
            gradient.addColorStop(1, "#999999");
            ctx.fillStyle = gradient;
            var hh = this.height / 2;
            ctx.arc(this.pos.x + hh, this.pos.y + hh, hh, 0.5 * Math.PI, 1.5 * Math.PI);
            ctx.rect(this.pos.x + hh, this.pos.y, this.width - this.height, this.height);
            ctx.arc(this.pos.x + this.width - hh, this.pos.y + hh, hh, 1.5 * Math.PI, 0.5 * Math.PI);
            ctx.fill();
            ctx.stroke();
        },
        left: function () {
            return this.pos.x;
        },
        right: function () {
            return this.pos.x + this.width;
        },
        top: function () {
            return this.pos.y;
        },
        bottom: function () {
            return this.pos.y + this.height;
        },
        test_hit: function () {
            var hitx = this.test_hit_x();
            var hity = this.test_hit_y();
            if (!hitx || !hity) {
                return 0;
            }
            if (hity) {
                ball.vel.y = -Math.abs(ball.vel.y);
                ball.pos.y += ball.vel.y;
                ball.pos.x -= ball.vel.x;
            }
            if (hitx) {
                var xdiff = ball.pos.x - (this.pos.x + (this.width / 2));
                ball.vel.x = (xdiff > 0 ? Math.ceil(xdiff / 5) : Math.floor(xdiff / 5)) * difficulty[currDiff]['speed_multiplier'];
                ball.pos.x += ball.vel.x;
            }
            return 1;
        },
        test_hit_x: function () {
            if (this.left() > ball.right()) {
                return 0;
            }
            if (this.right() < ball.left()) {
                return 0;
            }
            return 1;
        },
        test_hit_y: function () {
            if (this.top() > ball.bottom()) {
                return 0;
            }
            if (this.bottom() < ball.top()) {
                return 0;
            }
            return 1;
        },
        move: function () {
            if (pressLeft) {
                if (this.pos.x > 0) {
                    this.pos.x -= 8;
                }
            }
            if (pressRight) {
                if (this.pos.x < c.width - this.width) {
                    this.pos.x += 8;
                }
            }
        }
    };

    function fire() {
        this.r = 0;
        this.a = 0;
        this.render = function () {
            if (this.a < 0.2) {
                this.reset();
            }

            this.pos.x += this.vel.x + (Math.random() * 2) - 1;
            this.pos.y += this.vel.y + (Math.random() * 2) - 1;

            this.r *= 0.95;
            this.a *= 0.95;

            ctx.beginPath();
            ctx.fillStyle = 'rgba(' + (239 - this.green) + ', ' + this.green + ', 66,' + this.a + ')';
            ctx.arc(this.pos.x, this.pos.y, this.r, 0, 2 * Math.PI);
            ctx.fill();

            if (this.green < 232) {
                this.green += 8;
            }
        };
        this.reset = function () {
            this.pos = {
                x: ball.pos.x,
                y: ball.pos.y,
            };
            this.vel = {
                x: (Math.random() * 4) - 2,
                y: (Math.random() * 4) - 2,
            };
            this.r = (Math.random() * 5) + 1;
            this.a = 0.9;
            this.green = 62;
        };
    }

    function brick() {
        this.id = 0;
        this.pos = {
            x: 40,
            y: 40,
        };
        this.vely = 0;
        this.rot = 0;
        this.velr = 0;
        this.hit = false;
        this.last_hitx = false;
        this.last_hity = false;
        this.width = 40;
        this.height = 20;
        this.render = function () {
            if (this.hit) {
                if (this.pos.y > c.height + 60) {
                    return;
                }
                this.vely++;
                this.pos.y += this.vely;
                ctx.save();
                ctx.beginPath();
                this.rot += this.velr;
                ctx.translate(this.pos.x + (this.width / 2), this.pos.y + (this.height / 2));
                ctx.rotate(this.rot * Math.PI);
                var gradient = ctx.createRadialGradient(-(this.width / 2) + 10, -(this.height / 2) + 5, 0, -(this.width / 2) + 40, -(this.height / 2) + 15, 40);
                gradient.addColorStop(0, 'rgba(137, 211, 234, 0.2)');
                gradient.addColorStop(1, 'rgba(137, 211, 234, 1)');
                ctx.strokeStyle = 'rgba(254, 254, 254, 0.8)';
                ctx.fillStyle = gradient;
                ctx.rect(-(this.width / 2), -(this.height / 2), this.width, this.height);
                ctx.fill();
                ctx.stroke();
                ctx.restore();
                return;
            }
            ctx.beginPath();
            var gradient = ctx.createRadialGradient(this.pos.x + 10, this.pos.y + 5, 0, this.pos.x + 40, this.pos.y + 15, 40);
            gradient.addColorStop(0, 'rgba(137, 211, 234, 0.2)');
            gradient.addColorStop(1, 'rgba(137, 211, 234, 1)');
            ctx.strokeStyle = 'rgba(254, 254, 254, 0.8)';
            ctx.fillStyle = gradient;
            ctx.rect(this.pos.x, this.pos.y, this.width, this.height);
            ctx.fill();
            ctx.stroke();
        };
        this.test_hit = function () {
            if (this.hit) {
                return 0;
            }
            var hitx = this.test_hit_x();
            var hity = this.test_hit_y();
            if (!hitx || !hity) {
                this.last_hitx = hitx;
                this.last_hity = hity;
                return 0;
            }
            if (this.last_hity) {
                ball.vel.y = -ball.vel.y;
                ball.pos.y += ball.vel.y;
                ball.pos.x -= ball.vel.x;
            }
            if (this.last_hitx) {
                ball.vel.x = -ball.vel.x;
                ball.pos.x += ball.vel.x;
                ball.pos.y -= ball.vel.y;
            }
            if (!this.last_hity && this.last_hitx) {
                ball.vel.x = -ball.vel.x;
                ball.pos.x += ball.vel.x;
                ball.vel.y = -ball.vel.y;
                ball.pos.y += ball.vel.y;
            }
            this.last_hitx = hitx;
            this.last_hity = hity;
            this.hit = true;
            this.velr = (Math.random() * 0.04) - 0.02;
            score++;
            return 1;
        };
        this.test_hit_x = function () {
            if (this.left() > ball.right()) {
                return 0;
            }
            if (this.right() < ball.left()) {
                return 0;
            }
            return 1;
        };
        this.test_hit_y = function () {
            if (this.top() > ball.bottom()) {
                return 0;
            }
            if (this.bottom() < ball.top()) {
                return 0;
            }
            return 1;
        };
        this.left = function () {
            return this.pos.x;
        };
        this.right = function () {
            return this.pos.x + this.width;
        };
        this.top = function () {
            return this.pos.y;
        };
        this.bottom = function () {
            return this.pos.y + this.height;
        };
    }

    var pressLeft = false;
    var pressRight = false;

    document.addEventListener('keydown', (event) => {
        const keyName = event.key;
        if (keyName == "ArrowLeft") {
            pressLeft = true;
        }
        if (keyName == "ArrowRight") {
            pressRight = true;
        }
    });

    document.addEventListener('keyup', (event) => {
        const keyName = event.key;
        if (keyName == "ArrowLeft") {
            pressLeft = false;
        }
        if (keyName == "ArrowRight") {
            pressRight = false;
        }
        if (keyName == " ") {
            if (pause && !gameover) {
                if (!startTime) {
                    startTime = Math.floor(Date.now() / 1000);
                }
                pause = false;
                frame();
            } else {
                pause = true;
            }
        }
    });

    var bricks = [];

    for (var h = 0; h < 6; h++) {
        for (var w = 0; w < 18; w++) {
            var brickid = (18 * h) + w;
            bricks[brickid] = new brick();
            bricks[brickid].pos.x = 40 + (w * 40);
            bricks[brickid].pos.y = 40 + (h * 20);
            bricks[brickid].id = brickid;
        }
    }
    var fires = [];

    for (var i = 0; i < 80; i++) {
        fires[i] = new fire();
    }
    var startFireCount = 1;

    var pause = true;
    var gameover = false;

    var frame = function () {
        if (score >= bricks.length) {
            endGame();
        }
        ctx.clearRect(0, 0, c.width, c.height);
        for (var i = 0; i < bricks.length; i++) {
            bricks[i].render();
        }
        for (var i = 0; i < bricks.length; i++) {
            if (bricks[i].test_hit()) {
                break;
            }
        }
        for (var i = 0; i < fires.length && i < startFireCount; i++) {
            fires[i].render();
        }
        if (startFireCount <= fires.length) {
            startFireCount++;
        }
        paddle.move();
        paddle.render();
        paddle.test_hit();
        ball.render();

        if (pause) {
            if (!gameover) {
                ctx.font = "50px Gugi";
                ctx.fillStyle = '#FFFFFF';
                ctx.textAlign = "center";
                ctx.fillText("Ready " + currUserName, c.width / 2, c.height / 2);
                ctx.fillText("Press Space to Start", c.width / 2, c.height / 2 + 60);
            }
        } else {
            requestAnimationFrame(frame);
        }
    };

    var startTime = false;
    document.fonts.load('50px Gugi').then(frame);

    var endGame = function () {
        pause = true;
        gameover = true;
        submitScore();
    };

    var refreshScoreBoard = function () {
        var scores = JSON.parse(this.responseText);
        console.log(scores);
        var output = '<tr><th>Score</th><th>Time</th><th>Name</th></tr>';
        for (var i = 0; i < scores.length; i++) {
            output += '<tr><td>' + scores[i].score + '</td><td>' + scores[i].time + 's</td><td>' + scores[i].name + '</td></tr>';
        }
        document.getElementById("leadertable").innerHTML = output;
    };

    var submitScore = function () {
        var time_taken = Math.floor(Date.now() / 1000) - startTime;
        var xhttp = new XMLHttpRequest();
        xhttp.addEventListener("load", getScoreBoard);
        xhttp.open("POST", "/api/score/" + launchId + "/" + score + "/" + time_taken + "/", false);
        xhttp.send();
    };

    var getScoreBoard = function () {
        var xhttp = new XMLHttpRequest();
        xhttp.addEventListener("load", refreshScoreBoard);
        xhttp.open("GET", "/api/scoreboard/" + launchId + "/", true);
        xhttp.send();
    };

    getScoreBoard();
}

document.addEventListener("DOMContentLoaded", mainGame);
