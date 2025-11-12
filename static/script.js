console.log('Script loaded successfully!');

document.addEventListener('DOMContentLoaded', function() {
    loadStats();
    loadEnemies()
    loadGameState();
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

async function resetGame() {
    try {
        console.log('Resetting game...');

        const response = await fetch('/api/game/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();
        console.log('Reset result:', result);

        const battleLog = document.getElementById('battle-log');

        if (result.success) {
            battleLog.innerHTML = `<p class="respawn-message">${result.message}</p>`;
            // Обновляем статистику и врагов после сброса
            loadStats();
            loadEnemies()
            loadGameState();
        } else {
            battleLog.innerHTML = `<p class="error-message">Error resetting game</p>`;
        }

    } catch (error) {
        console.error('Error resetting game:', error);
        document.getElementById('battle-log').innerHTML =
            `<p class="error-message">Error: ${error.message}</p>`;
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
        loadEnemies();
        loadGameState()

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
        loadEnemies()
        loadGameState();

    } catch (error) {
        console.error('Error attacking enemy:', error);
        document.getElementById('battle-log').innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
    }
}

async function loadGameState() {
    try {
        const response = await fetch('/api/game/state');
        const state = await response.json();

        document.getElementById('current-wave').textContent = state.current_wave;
        document.getElementById('total-waves').textContent = state.total_waves;
        document.getElementById('wave-name').textContent = state.wave_name;
        document.getElementById('wave-kills').textContent = state.killed_in_wave;
        document.getElementById('wave-required').textContent = state.required_kills;

        // Прогресс бар
        const progressPercent = state.required_kills > 0 ?
            (state.killed_in_wave / state.required_kills) * 100 : 0;
        document.getElementById('wave-progress').style.width = `${progressPercent}%`;

    } catch (error) {
        console.error('Error loading game state:', error);
    }
}

// Обновляем attackSpecificEnemy чтобы обрабатывать волны
async function attackSpecificEnemy(enemyId) {
    try {
        const response = await fetch(`/api/attack/${enemyId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const result = await response.json();
        const battleLog = document.getElementById('battle-log');

        if (result.message) {
            let message = `<p class="battle-message">${result.message}</p>`;

            // Добавляем сообщение о новой волне если есть
            if (result.wave_message) {
                message += `<p class="respawn-message">🎉 ${result.wave_message}</p>`;
            }

            battleLog.innerHTML = message;
        }

        loadStats();
        loadEnemies();
        loadGameState(); // Обновляем информацию о волне

    } catch (error) {
        console.error('Error attacking enemy:', error);
    }
}
