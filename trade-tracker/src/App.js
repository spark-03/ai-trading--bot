import React, { useState, useEffect } from "react";

function App() {
  const [trades, setTrades] = useState([]); // ✅ State for trades

  // ✅ Fetch trades every 5 seconds (Auto-refresh)
  useEffect(() => {
    const fetchTrades = async () => {
      try {
        const response = await fetch("http://localhost:5000/trades");
        if (!response.ok) throw new Error("Failed to fetch trades!");
        const data = await response.json();
        setTrades(data);
      } catch (error) {
        console.error("⚠️ Error fetching trades:", error);
      }
    };

    fetchTrades(); // Fetch once on load
    const interval = setInterval(fetchTrades, 5000); // Auto-refresh every 5 sec

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  return (
    <div className="container">
      <h1>📊 Real-Time Trade Tracker</h1>

      {/* Trade Table */}
      <table className="trade-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Symbol</th>
            <th>Buy Price</th>
            <th>Sell Price</th>
            <th>Profit/Loss</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {trades.length > 0 ? (
            trades.map((trade) => (
              <tr key={trade.id}>
                <td>{trade.id}</td>
                <td>{trade.symbol.toUpperCase()}</td>
                <td>₹{parseFloat(trade.buyPrice).toFixed(2)}</td>
                <td>₹{parseFloat(trade.sellPrice).toFixed(2)}</td>
                <td
                  style={{
                    color: trade.profitLoss >= 0 ? "green" : "red",
                    fontWeight: "bold",
                  }}
                >
                  ₹{trade.profitLoss}
                </td>
                <td>{new Date(trade.time).toLocaleString()}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6">📉 No trades recorded yet!</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default App;
