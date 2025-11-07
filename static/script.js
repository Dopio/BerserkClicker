console.log('Script loaded successfully!');

document.addEventListener('DOMContentLoaded', function() {
    loadStats();
    loadEnemies();
});

// Функция загрузки статистики игрока
async function loadStats() {
    try {
        const response = await fetch('/api/player/stats');
        const data = await response.json();

        document.getElementById('player-name').textContent = data.player_name;
        document.getElementById('player-health').textContent = data.player_health;
        document.getElementById('player-blood').textContent = data.player_blood;
        document.getElementById('player-kills').textContent = data.player_kills;
        document.getElementById('player-damage').textContent = data.player_damage;
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
        loadEnemies(); // ← ДОБАВЬ: обновляем список врагов после боя

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

async function loadEnemies() {
    try {
        console.log('Loading enemies...');
        const response = await fetch('/api/enemies');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const enemies = await response.json();
        console.log('Enemies loaded:', enemies);

        const enemiesList = document.getElementById('enemies-list');
        enemiesList.innerHTML = '';

        if (enemies.length === 0) {
            enemiesList.innerHTML = '<p>No enemies available</p>';
            return;
        }

        enemies.forEach(enemy => {
            console.log('Processing enemy:', enemy);
            const enemyElement = document.createElement('div');
            enemyElement.className = `enemy ${enemy.enemy_is_alive ? 'alive' : 'dead'}`;

            enemyElement.innerHTML = `
                <h3>${enemy.enemy_name}</h3>
                <p>HP: ${enemy.enemy_health} | Damage: ${enemy.enemy_damage}</p>
                ${enemy.enemy_is_alive ?
                    `<button onclick="attackSpecificEnemy(${enemy.enemy_id})">⚔️ Attack</button>` :
                    `<span class="dead-text">💀 DEAD</span>`
                }
            `;

            enemiesList.appendChild(enemyElement);
        });

    } catch (error) {
        console.error('Error loading enemies:', error);
        document.getElementById('enemies-list').innerHTML = '<p class="error-message">Error loading enemies</p>';
    }
}

async function attackSpecificEnemy(enemyId) {
    try {
        console.log(`Attacking enemy with ID: ${enemyId}`);
        const response = await fetch(`/api/attack/${enemyId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();
        console.log('Attack result:', result);

        const battleLog = document.getElementById('battle-log');

        if (result.message) {
            battleLog.innerHTML = `<p class="battle-message">${result.message}</p>`;
        } else if (result.error) {
            battleLog.innerHTML = `<p class="error-message">❌ ${result.error}</p>`;
        }

        loadStats();
        loadEnemies();

    } catch (error) {
        console.error('Error attacking enemy:', error);
        document.getElementById('battle-log').innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
    }
}