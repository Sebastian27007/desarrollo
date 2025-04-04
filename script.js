document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('minesweeper');
    const resetButton = document.getElementById('resetButton');
    const width = 10;
    const height = 10;
    const minesCount = 20;
    let cells = [];
    let gameOver = false;

    function createGrid() {
        grid.innerHTML = '';
        cells = [];
        gameOver = false;

        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.dataset.x = x;
                cell.dataset.y = y;
                grid.appendChild(cell);
                cells.push(cell);
            }
        }

        let minesPlaced = 0;
        while (minesPlaced < minesCount) {
            const index = Math.floor(Math.random() * cells.length);
            if (!cells[index].classList.contains('mine')) {
                cells[index].classList.add('mine');
                minesPlaced++;
            }
        }

        cells.forEach(cell => {
            cell.addEventListener('click', () => {
                if (gameOver) return;
                if (cell.classList.contains('mine')) {
                    cell.classList.add('revealed');
                    alert('Game Over!');
                    gameOver = true;
                } else {
                    cell.classList.add('revealed');
                }
            });
        });
    }

    resetButton.addEventListener('click', createGrid);

    createGrid();
});
