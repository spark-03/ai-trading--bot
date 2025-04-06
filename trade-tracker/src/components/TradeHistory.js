import React, { useEffect, useState } from "react";

const TradeHistory = () => {
    const [trades, setTrades] = useState([]);

    // Load trades from local storage
    useEffect(() => {
        const savedTrades = JSON.parse(localStorage.getItem("trades")) || [];
        setTrades(savedTrades);
    }, []);

    return (
        <div>
            <h2>Trade History</h2>
            <table border="1">
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
                    {trades.map((trade, index) => (
                        <tr key={index}>
                            <td>{index + 1}</td>
                            <td>{trade.symbol}</td>
                            <td>{trade.buyPrice}</td>
                            <td>{trade.sellPrice}</td>
                            <td style={{ color: trade.profit >= 0 ? "green" : "red" }}>
                                {trade.profit >= 0 ? `+${trade.profit}` : trade.profit}
                            </td>
                            <td>{trade.time}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default TradeHistory;
