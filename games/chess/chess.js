const boardElem = document.getElementById('board');
let selected = null;
let state = null;

const PIECES = {
    "r": "\u265C", "n": "\u265E", "b": "\u265D", "q": "\u265B", "k": "\u265A", "p": "\u265F",
    "R": "\u2656", "N": "\u2658", "B": "\u2657", "Q": "\u2655", "K": "\u2654", "P": "\u2659"
};

async function loadState() {
    const res = await fetch('/api/chess');
    state = await res.json();
    renderBoard();
}

async function saveState() {
    await fetch('/api/chess', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(state)
    });
}

function renderBoard() {
    boardElem.innerHTML = '';
    for (let r = 0; r < 8; r++) {
        const row = document.createElement('tr');
        for (let c = 0; c < 8; c++) {
            const cell = document.createElement('td');
            cell.className = (r + c) % 2 === 0 ? 'light' : 'dark';
            cell.dataset.row = r;
            cell.dataset.col = c;
            const piece = state.board[r][c];
            cell.textContent = PIECES[piece] || '';
            cell.addEventListener('click', onCellClick);
            row.appendChild(cell);
        }
        boardElem.appendChild(row);
    }
}

function onCellClick(e) {
    const r = parseInt(e.currentTarget.dataset.row);
    const c = parseInt(e.currentTarget.dataset.col);
    if (selected) {
        if (movePiece(selected.r, selected.c, r, c)) {
            selected.elem.classList.remove('selected');
            selected = null;
            renderBoard();
            saveState();
            setTimeout(aiMove, 500);
        } else {
            selected.elem.classList.remove('selected');
            selected = null;
        }
    } else {
        const piece = state.board[r][c];
        if (piece && piece === piece.toUpperCase() && state.turn === 'white') {
            selected = {r, c, elem: e.currentTarget};
            e.currentTarget.classList.add('selected');
        }
    }
}

function movePiece(fr, fc, tr, tc) {
    const piece = state.board[fr][fc];
    const target = state.board[tr][tc];
    const moves = getMoves(piece, fr, fc);
    for (const m of moves) {
        if (m[0] === tr && m[1] === tc) {
            if (target && target === target.toUpperCase()) return false; // own piece
            state.board[tr][tc] = piece;
            state.board[fr][fc] = '';
            state.turn = 'black';
            return true;
        }
    }
    return false;
}

function getMoves(piece, r, c) {
    const moves = [];
    const dirs = [];
    const add = (dr, dc) => { dirs.push([dr, dc]); };
    if (piece === 'P') {
        if (r>0 && !state.board[r-1][c]) moves.push([r-1,c]);
        if (r===6 && !state.board[r-1][c] && !state.board[r-2][c]) moves.push([r-2,c]);
        if (r>0 && c>0 && state.board[r-1][c-1] && state.board[r-1][c-1]===state.board[r-1][c-1].toLowerCase()) moves.push([r-1,c-1]);
        if (r>0 && c<7 && state.board[r-1][c+1] && state.board[r-1][c+1]===state.board[r-1][c+1].toLowerCase()) moves.push([r-1,c+1]);
        return moves;
    }
    if (piece === 'R' || piece === 'r') { add(1,0); add(-1,0); add(0,1); add(0,-1); }
    if (piece === 'B' || piece === 'b') { add(1,1); add(1,-1); add(-1,1); add(-1,-1); }
    if (piece === 'Q' || piece === 'q') { add(1,0); add(-1,0); add(0,1); add(0,-1); add(1,1); add(1,-1); add(-1,1); add(-1,-1); }
    if (piece === 'K' || piece === 'k') {
        const d = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]];
        for (const [dr,dc] of d) {
            const nr=r+dr, nc=c+dc;
            if (nr>=0 && nr<8 && nc>=0 && nc<8 && (!state.board[nr][nc] || piece.toUpperCase()!==state.board[nr][nc].toUpperCase())) moves.push([nr,nc]);
        }
        return moves;
    }
    if (piece === 'N' || piece === 'n') {
        const d=[[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]];
        for (const [dr,dc] of d) {
            const nr=r+dr,nc=c+dc;
            if (nr>=0 && nr<8 && nc>=0 && nc<8 && (!state.board[nr][nc] || piece.toUpperCase()!==state.board[nr][nc].toUpperCase())) moves.push([nr,nc]);
        }
        return moves;
    }
    // sliding pieces
    for (const [dr, dc] of dirs) {
        let nr=r+dr, nc=c+dc;
        while (nr>=0 && nr<8 && nc>=0 && nc<8) {
            const t=state.board[nr][nc];
            if (!t) {
                moves.push([nr,nc]);
            } else {
                if (piece.toUpperCase()!==t.toUpperCase()) moves.push([nr,nc]);
                break;
            }
            nr+=dr; nc+=dc;
        }
    }
    return moves;
}

function aiMove() {
    if (state.turn !== 'black') return;
    const moves = [];
    for (let r=0;r<8;r++) {
        for (let c=0;c<8;c++) {
            const piece = state.board[r][c];
            if (piece && piece === piece.toLowerCase()) {
                const m = getMoves(piece, r, c);
                for (const [tr,tc] of m) moves.push({fr:r,fc:c,tr,tc});
            }
        }
    }
    if (moves.length===0) return;
    const choice = moves[Math.floor(Math.random()*moves.length)];
    state.board[choice.tr][choice.tc] = state.board[choice.fr][choice.fc];
    state.board[choice.fr][choice.fc] = '';
    state.turn = 'white';
    renderBoard();
    saveState();
}

loadState();
