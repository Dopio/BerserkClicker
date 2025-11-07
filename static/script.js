document.addEventListener('DOMContentLoaded', function() {
    loadStats();
});

// Функция загрузки статистики игрока
async function loadStats() {
    try {
        const response = await fetch('/api/player/stats');
        const data = await response.json();
        
        document.getElementById('player-name').textContent = data.name;
        document.getElementById('player-health').textContent = data.health;
        document.getElementById('player-blood').textContent = data.blood;
        document.getElementById('player-kills').textContent = data.kills;
        document.getElementById('player-damage').textContent = data.damage;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Функция атаки случайного врага
async function attackRandom() {
    try {
        const response = await fetch('/api/attack/random', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        const battleLog = document.getElementById('battle-log');

        if (result.message) {
            battleLog.innerHTML = `<p class="battle-message">${result.message}</p>`;
        } else if (result.error) {
            battleLog.innerHTML = `<p class="battle-message">❌ ${result.error}</p>`;
        }

        loadStats();
        
    } catch (error) {
        console.error('Error attacking:', error);
    }
}


async function buyDamageUpgrade() {
    try {
        const response = await fetch('/api/upgrade/damage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        const battleLog = document.getElementById('battle-log');
        battleLog.innerHTML = `<p class="battle-message">${result.message}</p>`;

        loadStats();

    } catch (error) {
        console.error('Error upgrading:', error);
    }
}


async function buyHealthUpgrade() {
    try {
        const response = await fetch('/api/upgrade/health', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        const battleLog = document.getElementById('battle-log');
        battleLog.innerHTML = `<p class="battle-message">${result.message}</p>`;

        loadStats();

    } catch (error) {
        console.error('Error upgrading:', error);
    }
}

