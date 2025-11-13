import { useState, useEffect } from 'react'
import './App.css'

interface Portfolio {
  capital: number
  available_capital: number
  invested_capital: number
  total_value: number
  unrealized_pnl: number
  realized_pnl: number
  total_pnl: number
  total_return_percent: number
  open_positions: number
}

interface Position {
  symbol: string
  quantity: number
  entry_price: number
  current_price: number
  pnl: number
  pnl_percent: number
  stop_loss: number
  take_profit: number
}

interface Symbol {
  symbol: string
  name: string
}

interface MarketData {
  symbol: string
  name: string
  price: number
  change: number
  change_percent: number
}

function App() {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null)
  const [positions, setPositions] = useState<Position[]>([])
  const [symbols, setSymbols] = useState<Symbol[]>([])
  const [marketData, setMarketData] = useState<Record<string, MarketData>>({})
  const [isRunning, setIsRunning] = useState(false)
  const [ws, setWs] = useState<WebSocket | null>(null)

  useEffect(() => {
    fetchInitialData()
    connectWebSocket()

    return () => {
      if (ws) {
        ws.close()
      }
    }
  }, [])

  const fetchInitialData = async () => {
    try {
      const [portfolioRes, symbolsRes, statusRes] = await Promise.all([
        fetch('/api/portfolio'),
        fetch('/api/symbols'),
        fetch('/api/bot/status')
      ])

      const portfolioData = await portfolioRes.json()
      const symbolsData = await symbolsRes.json()
      const statusData = await statusRes.json()

      setPortfolio(portfolioData.portfolio)
      setPositions(portfolioData.positions)
      setSymbols(symbolsData)
      setIsRunning(statusData.is_running)

      for (const symbol of symbolsData) {
        const res = await fetch(`/api/market/${symbol.symbol}`)
        const data = await res.json()
        setMarketData(prev => ({ ...prev, [symbol.symbol]: data }))
      }
    } catch (error) {
      console.error('Error fetching initial data:', error)
    }
  }

  const connectWebSocket = () => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}/ws`
    
    const websocket = new WebSocket(wsUrl)

    websocket.onopen = () => {
      console.log('WebSocket connected')
    }

    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data)
      
      if (message.type === 'portfolio_update') {
        setPortfolio(message.data.portfolio)
        setPositions(message.data.positions)
        if (message.data.market_data) {
          setMarketData(prev => ({ ...prev, ...message.data.market_data }))
        }
      } else if (message.type === 'trade_executed') {
        console.log('Trade executed:', message.data)
      }
    }

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    websocket.onclose = () => {
      console.log('WebSocket disconnected, reconnecting...')
      setTimeout(connectWebSocket, 3000)
    }

    setWs(websocket)
  }

  const toggleBot = async () => {
    try {
      const endpoint = isRunning ? '/api/bot/stop' : '/api/bot/start'
      const res = await fetch(endpoint, { method: 'POST' })
      const data = await res.json()
      setIsRunning(data.is_running)
    } catch (error) {
      console.error('Error toggling bot:', error)
    }
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2
    }).format(value)
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🚀 Upstox Trading Bot</h1>
        <div className="header-controls">
          <span className={`status-badge ${isRunning ? 'running' : 'stopped'}`}>
            {isRunning ? '● Running' : '○ Stopped'}
          </span>
          <button onClick={toggleBot} className={isRunning ? 'btn-stop' : 'btn-start'}>
            {isRunning ? 'Stop Bot' : 'Start Bot'}
          </button>
        </div>
      </header>

      <div className="dashboard">
        {portfolio && (
          <div className="portfolio-summary">
            <h2>Portfolio Summary</h2>
            <div className="portfolio-grid">
              <div className="portfolio-card">
                <div className="card-label">Total Value</div>
                <div className="card-value">{formatCurrency(portfolio.total_value)}</div>
              </div>
              <div className="portfolio-card">
                <div className="card-label">Total P&L</div>
                <div className={`card-value ${portfolio.total_pnl >= 0 ? 'positive' : 'negative'}`}>
                  {formatCurrency(portfolio.total_pnl)}
                </div>
              </div>
              <div className="portfolio-card">
                <div className="card-label">Return</div>
                <div className={`card-value ${portfolio.total_return_percent >= 0 ? 'positive' : 'negative'}`}>
                  {portfolio.total_return_percent.toFixed(2)}%
                </div>
              </div>
              <div className="portfolio-card">
                <div className="card-label">Available Capital</div>
                <div className="card-value">{formatCurrency(portfolio.available_capital)}</div>
              </div>
              <div className="portfolio-card">
                <div className="card-label">Invested</div>
                <div className="card-value">{formatCurrency(portfolio.invested_capital)}</div>
              </div>
              <div className="portfolio-card">
                <div className="card-label">Positions</div>
                <div className="card-value">{portfolio.open_positions}</div>
              </div>
            </div>
          </div>
        )}

        {positions.length > 0 && (
          <div className="positions-section">
            <h2>Active Positions</h2>
            <div className="table-container">
              <table className="positions-table">
                <thead>
                  <tr>
                    <th>Symbol</th>
                    <th>Quantity</th>
                    <th>Entry Price</th>
                    <th>Current Price</th>
                    <th>P&L</th>
                    <th>P&L %</th>
                    <th>Stop Loss</th>
                    <th>Take Profit</th>
                  </tr>
                </thead>
                <tbody>
                  {positions.map((pos) => (
                    <tr key={pos.symbol}>
                      <td className="symbol-cell">{pos.symbol}</td>
                      <td>{pos.quantity}</td>
                      <td>{formatCurrency(pos.entry_price)}</td>
                      <td>{formatCurrency(pos.current_price)}</td>
                      <td className={pos.pnl >= 0 ? 'positive' : 'negative'}>
                        {formatCurrency(pos.pnl)}
                      </td>
                      <td className={pos.pnl_percent >= 0 ? 'positive' : 'negative'}>
                        {pos.pnl_percent.toFixed(2)}%
                      </td>
                      <td>{formatCurrency(pos.stop_loss)}</td>
                      <td>{formatCurrency(pos.take_profit)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        <div className="market-overview">
          <h2>Market Overview</h2>
          <div className="market-grid">
            {symbols.map((symbol) => {
              const data = marketData[symbol.symbol]
              return (
                <div key={symbol.symbol} className="market-card">
                  <div className="market-symbol">{symbol.symbol}</div>
                  <div className="market-name">{symbol.name}</div>
                  {data && (
                    <>
                      <div className="market-price">{formatCurrency(data.price)}</div>
                      <div className={`market-change ${data.change >= 0 ? 'positive' : 'negative'}`}>
                        {data.change >= 0 ? '+' : ''}{data.change.toFixed(2)} ({data.change_percent.toFixed(2)}%)
                      </div>
                    </>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
