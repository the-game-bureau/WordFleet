// Game configuration
const WORD_LISTS = {
    5: ['SWORD', 'CROWN', 'STORM', 'OCEAN', 'BRAVE', 'MAGIC', 'QUEST', 'FLEET', 'ANCHOR', 'CASTLE'],
    4: ['SHIP', 'GOLD', 'WAVE', 'WIND', 'FORT', 'SAIL', 'DECK', 'CREW', 'PORT', 'TIDE'],
    3: ['SEA', 'MAP', 'SUN', 'WAR', 'BAY', 'FOG', 'GUN', 'AXE', 'BOW', 'KEY'],
    2: ['AX', 'OX', 'BY', 'GO', 'UP', 'IN', 'ON', 'OR', 'SO', 'TO']
};

// Game initialization
window.addEventListener('load', function() {
    showModal();
    updateCoinFlip();
});

// Modal functions
function showModal() {
    document.getElementById('modal').style.display = 'flex';
}

function hideModal() {
    document.getElementById('modal').style.display = 'none';
}

// Coin flip logic
function updateCoinFlip() {
    const isHeads = Math.random() < 0.5;
    const coinFlip1 = document.getElementById('coinFlip1');
    const coinFlip2 = document.getElementById('coinFlip2');
    
    coinFlip1.textContent = isHeads ? "IF HEADS YOU'RE FIRST" : "IF TAILS YOU'RE FIRST";
    coinFlip2.textContent = isHeads ? "IF TAILS YOU'RE FIRST" : "IF HEADS YOU'RE FIRST";
    
    return isHeads;
}

// Main game setup function
function startGame() {
    const player1Name = getPlayerName('player1Name');
    const player2Name = getPlayerName('player2Name');
    const autoGenerate = document.getElementById('autoGen').checked;
    
    updateFleetTitles(player1Name, player2Name);
    
    if (autoGenerate) {
        generateAllWords();
    }
    
    hideModal();
    
    // Print after a brief delay to ensure all updates are applied
    setTimeout(() => {
        window.print();
    }, 100);
}

// Helper functions
function getPlayerName(inputId) {
    return document.getElementById(inputId).value.trim();
}

function updateFleetTitles(player1Name, player2Name) {
    // Update titles - each player sees the other as their opponent
    if (player1Name) {
        document.getElementById('your-title1').textContent = player1Name;
        document.getElementById('opponent-title2').textContent = player1Name;
    }
    
    if (player2Name) {
        document.getElementById('your-title2').textContent = player2Name;
        document.getElementById('opponent-title1').textContent = player2Name;
    }
}

// Word generation functions
function generateAllWords() {
    generatePlayerWords('p1');
    generatePlayerWords('p2');
}

function generatePlayerWords(player) {
    const usedWords = new Set();
    
    const getUniqueWord = (length) => {
        let attempts = 0;
        let word;
        
        do {
            word = getRandomWord(length);
            attempts++;
        } while (usedWords.has(word) && attempts < 20);
        
        usedWords.add(word);
        return word;
    };
    
    // Generate words for each ship type
    fillWord(`your-5-${player}`, getUniqueWord(5));
    fillWord(`your-4-${player}`, getUniqueWord(4));
    
    // Generate two different 3-letter words
    const word3a = getUniqueWord(3);
    fillWord(`your-3a-${player}`, word3a);
    
    let word3b;
    do {
        word3b = getUniqueWord(3);
    } while (word3b === word3a);
    fillWord(`your-3b-${player}`, word3b);
    
    fillWord(`your-2-${player}`, getUniqueWord(2));
}

function getRandomWord(length) {
    const wordList = WORD_LISTS[length];
    const randomIndex = Math.floor(Math.random() * wordList.length);
    return wordList[randomIndex];
}

function fillWord(containerId, word) {
    const container = document.getElementById(containerId);
    
    if (!container) {
        console.warn(`Container with ID '${containerId}' not found`);
        return;
    }
    
    const boxes = container.children;
    
    for (let i = 0; i < word.length && i < boxes.length; i++) {
        boxes[i].textContent = word[i];
    }
}