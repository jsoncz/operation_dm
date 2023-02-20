// Set up the game canvas
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Set up the game board
const BLOCK_SIZE = 40;
const NUM_ROWS = 12;
const NUM_COLS = 8;
const BOARD_LEFT_MARGIN = 50;
const BOARD_TOP_MARGIN = 50;

// Define block colors
const RED = "rgb(255, 0, 0)";
const GREEN = "rgb(0, 255, 0)";
const BLUE = "rgb(0, 0, 255)";
const YELLOW = "rgb(255, 255, 0)";
const PURPLE = "rgb(255, 0, 255)";
const ORANGE = "rgb(255, 128, 0)";

class Block {
    constructor(color, row, col) {
        this.color = color;
        this.row = row;
        this.col = col;
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.col * BLOCK_SIZE + BOARD_LEFT_MARGIN,
                     this.row * BLOCK_SIZE + BOARD_TOP_MARGIN,
                     BLOCK_SIZE, BLOCK_SIZE);
    }

    moveLeft() {
        this.col -= 1;
    }

    moveRight() {
        this.col += 1;
    }
}

class Board {
    constructor(num_rows, num_cols, left_margin, top_margin) {
        this.num_rows = num_rows;
        this.num_cols = num_cols;
        this.left_margin = left_margin;
        this.top_margin = top_margin;
        this.blocks = [];
        this.specialItems = [];
    }

    addBlock(block) {
        this.blocks.push(block);
    }

    addSpecialItem(item) {
        this.specialItems.push(item);
    }

    draw() {
        for (let row = 0; row < this.num_rows; row++) {
            for (let col = 0; col < this.num_cols; col++) {
                ctx.beginPath();
                ctx.rect(col * BLOCK_SIZE + this.left_margin,
                         row * BLOCK_SIZE + this.top_margin,
                         BLOCK_SIZE, BLOCK_SIZE);
                ctx.stroke();
            }
        }

        for (let block of this.blocks) {
            block.draw();
        }

        for (let item of this.specialItems) {
            item.draw();
        }
    }

    update() {
        for (let i = this.blocks.length - 1; i >= 0; i--) {
            let block = this.blocks[i];
            if (block.row == this.num_rows - 1) {
                // Block has reached the bottom of the board
                this.blocks.splice(i, 1);
                continue;
            }

            // Check if block is colliding with another block
            let blockColliding = false;
            for (let otherBlock of this.blocks) {
                if (block === otherBlock) {
                    continue;
                }
                if (block.row + 1 == otherBlock.row && block.col == otherBlock.col) {
                    blockColliding = true;
                    break;
                }
            }
            if (!blockColliding) {
                block.row += 1;
            }
        }

        for (let item of this.specialItems) {
            if (item.row == this.num_rows - 1) {
                // Item has reached the bottom of the board
                this.specialItems.splice(this.specialItems.indexOf(item), 1);
                continue;
            }

            item.row += 1;
        }
    }


clearMatchingBlocks() {
    // TODO: Implement this function
}

removeBlock(block) {
    this.blocks.splice(this.blocks.indexOf(block), 1);
}

moveBlocksLeft() {
    for (let block of this.blocks) {
        if (block.col > 0) {
            block.moveLeft();
        }
    }
}
moveBlocksRight() {
    for (let block of this.blocks) {
        if (block.col < this.num_cols - 1) {
            block.moveRight();
        }
    }
}

clearMatchingBlocks() {
    // TODO: Implement this function
}

removeBlock(block) {
    this.blocks.splice(this.blocks.indexOf(block), 1);
}

moveBlocksLeft() {
    for (let block of this.blocks) {
        if (block.col > 0) {
            block.moveLeft();
        }
    }
}

moveBlocksRight() {
    for (let block of this.blocks) {
        if (block.col < this.num_cols - 1) {
            block.moveRight();
        }
    }
}
}

let player1_board = new Board(NUM_ROWS, NUM_COLS, BOARD_LEFT_MARGIN, BOARD_TOP_MARGIN);
let player2_board = new Board(NUM_ROWS, NUM_COLS, canvas.width - BOARD_LEFT_MARGIN - NUM_COLS * BLOCK_SIZE, BOARD_TOP_MARGIN);

let BLOCK_COLORS = [RED, GREEN, BLUE];

let gamepadConnected = false;
let gamepad = null;

// Set up gamepad input
window.addEventListener("gamepadconnected", (event) => {
console.log("Gamepad connected!");
gamepadConnected = true;
gamepad = event.gamepad;
});

window.addEventListener("gamepaddisconnected", (event) => {
console.log("Gamepad disconnected.");
gamepadConnected = false;
gamepad = null;
});

function handleInput() {
if (gamepadConnected) {
    // Handle gamepad input
    if (gamepad.axes[0] < -0.5) {
        player1_board.moveBlocksLeft();
    }
    else if (gamepad.axes[0] > 0.5) {
        player1_board.moveBlocksRight();
    }
}
else {
    // Handle keyboard input
    if (keysPressed["ArrowLeft"]) {
        player1_board.moveBlocksLeft();
    }
    else if (keysPressed["ArrowRight"]) {
        player1_board.moveBlocksRight();
    }
}
}

let lastTimestamp = 0;
let keysPressed = {};

function gameLoop(timestamp) {
// Calculate time delta
let delta = timestamp - lastTimestamp;
lastTimestamp = timestamp;

// Handle input
handleInput();

// Update game state
player1_board.update();
player2_board.update();

// Generate new blocks
for (let board of [player1_board, player2_board]) {
    if (board.blocks.length < 20) {
        // Generate a new column of blocks
        let newColumn = [];
        for (let i = 0; i < board.num_rows; i++) {
            if (Math.random() < 0.5) {
                let color = BLOCK_COLORS[Math.floor(Math.random() * BLOCK_COLORS.length)];
                let block = new Block(color, i, board.num_cols);
                newColumn.push(block);
            }
        }
        for (let block of newColumn) {
            board.addBlock(block);
        }
    }
}

// Clear canvas
ctx.clearRect(0, 0, canvas.width, canvas.height);

// Draw game objects
player1_board.draw();
player2_board.draw();

// Request next frame
window.requestAnimationFrame(gameLoop);
}

// Start the game loop
window.requestAnimationFrame(gameLoop);

// Set up keyboard input
document.addEventListener("keydown", (event) => {
keysPressed[event.key] = true;
});

document.addEventListener("keyup", (event) => {
keysPressed[event.key] = false;
});