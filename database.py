import aiosqlite
import json
from datetime import datetime
from typing import List, Dict, Any

class Database:
    def __init__(self, db_path: str = "trading_bot.db"):
        self.db_path = db_path
    
    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    action TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    pnl REAL DEFAULT 0,
                    signals TEXT,
                    status TEXT DEFAULT 'open'
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS positions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT UNIQUE NOT NULL,
                    quantity INTEGER NOT NULL,
                    entry_price REAL NOT NULL,
                    current_price REAL NOT NULL,
                    pnl REAL NOT NULL,
                    stop_loss REAL,
                    take_profit REAL,
                    timestamp TEXT NOT NULL
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    data TEXT
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    total_trades INTEGER,
                    winning_trades INTEGER,
                    total_pnl REAL,
                    win_rate REAL,
                    sharpe_ratio REAL
                )
            """)
            
            await db.commit()
    
    async def add_trade(self, symbol: str, action: str, quantity: int, price: float, signals: Dict[str, Any]):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO trades (timestamp, symbol, action, quantity, price, signals) VALUES (?, ?, ?, ?, ?, ?)",
                (datetime.now().isoformat(), symbol, action, quantity, price, json.dumps(signals))
            )
            await db.commit()
    
    async def update_position(self, symbol: str, quantity: int, entry_price: float, current_price: float, pnl: float, stop_loss: float, take_profit: float):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT OR REPLACE INTO positions 
                   (symbol, quantity, entry_price, current_price, pnl, stop_loss, take_profit, timestamp) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (symbol, quantity, entry_price, current_price, pnl, stop_loss, take_profit, datetime.now().isoformat())
            )
            await db.commit()
    
    async def remove_position(self, symbol: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM positions WHERE symbol = ?", (symbol,))
            await db.commit()
    
    async def get_positions(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM positions") as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def add_log(self, level: str, message: str, data: Dict[str, Any] = None):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO logs (timestamp, level, message, data) VALUES (?, ?, ?, ?)",
                (datetime.now().isoformat(), level, message, json.dumps(data) if data else None)
            )
            await db.commit()
    
    async def get_recent_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limit,)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def get_trades(self, limit: int = 100) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM trades ORDER BY id DESC LIMIT ?", (limit,)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def get_performance_stats(self) -> Dict[str, Any]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            
            async with db.execute("SELECT COUNT(*) as total, SUM(pnl) as total_pnl FROM trades WHERE status = 'closed'") as cursor:
                row = await cursor.fetchone()
                total_trades = row['total'] if row else 0
                total_pnl = row['total_pnl'] if row and row['total_pnl'] else 0.0
            
            async with db.execute("SELECT COUNT(*) as winning FROM trades WHERE status = 'closed' AND pnl > 0") as cursor:
                row = await cursor.fetchone()
                winning_trades = row['winning'] if row else 0
            
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
            
            return {
                "total_trades": total_trades,
                "winning_trades": winning_trades,
                "total_pnl": total_pnl,
                "win_rate": win_rate
            }

db = Database()
