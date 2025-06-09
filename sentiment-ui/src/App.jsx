import { useEffect, useState, useRef } from "react";
import { io } from "socket.io-client";
import { PieChart, Pie, Cell, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid, LineChart, Line } from "recharts";
import "./App.css";

const socket = io("http://127.0.0.1:5000");

function App() {
    const [data, setData] = useState([]);
    const [viewerCount, setViewerCount] = useState(0);
    const [channelLogo, setChannelLogo] = useState(null);
    const [videoTitle, setVideoTitle] = useState("");
    const chatEndRef = useRef(null);

    useEffect(() => {
        fetch("http://127.0.0.1:5000/chat")
            .then(response => response.json())
            .then(fetchedData => setData(fetchedData))
            .catch(error => console.error("Error fetching data:", error));

        socket.on("new_messages", (newMessages) => {
            setData((prevData) => {
                const existingMessages = new Set(prevData.map(msg => msg.message + msg.published_at));
                const filteredMessages = newMessages.filter(msg => !existingMessages.has(msg.message + msg.published_at));
                return [...prevData, ...filteredMessages];
            });
        });

        socket.on("viewer_count", (count) => {
            setViewerCount(count);
        });

        return () => {
            socket.off("new_messages");
            socket.off("viewer_count");
        };
    }, []);

    useEffect(() => {
        fetch("http://127.0.0.1:5000/video-info")
            .then(response => response.json())
            .then(data => {
                console.log("Video Info Response:", data); // Debugging

                if (data.title) {
                    setVideoTitle(data.title);
                    console.log("Updated Video Title:", data.title);
                } else {
                    console.error("No title found in response");
                }

                if (data.logo_url) {
                    setChannelLogo(data.logo_url);
                    console.log("Updated Channel Logo:", data.logo_url);
                } else {
                    console.error("No logo URL found in response");
                }
            })
            .catch(error => console.error("Error fetching video info:", error));
    }, []);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [data]);

    const positiveCount = data.filter(chat => chat.final_sentiment === "positive").length;
    const negativeCount = data.filter(chat => chat.final_sentiment === "negative").length;
    const neutralCount = data.filter(chat => chat.final_sentiment === "neutral").length;
    const totalMessages = positiveCount + negativeCount + neutralCount;

    const sentimentData = totalMessages > 0 ? [
        { name: "Positive", value: positiveCount, color: "#4CAF50" },
        { name: "Negative", value: negativeCount, color: "#E53935" },
        { name: "Neutral", value: neutralCount, color: "#FFC107" }
    ] : [];

    const sentimentBarData = [
        { name: "Positive", value: positiveCount },
        { name: "Negative", value: negativeCount },
        { name: "Neutral", value: neutralCount }
    ];

    const sentimentOverTime = data.map(chat => ({
        time: new Date(chat.published_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        sentiment: chat.final_sentiment === "positive" ? 1 : chat.final_sentiment === "negative" ? -1 : 0
    })).slice(-50);

    return (
        <div className="chat-wrapper">
            <div>
                <img src="/youtube_logo2.webp" alt="YouTube Logo" className="youtube-logo" />
                <div className="viewer-count">
                    <h2>{viewerCount}</h2>
                    <p>Viewers</p>
                </div>
                
                <div className="message-count">
                    <h2>{totalMessages}</h2>
                    <p>Total Messages</p>
                    <div className="sentiment-stats">
                        <p className="positive-text">Positive: {positiveCount}</p>
                        <p className="negative-text">Negative: {negativeCount}</p>
                        <p className="neutral-text">Neutral: {neutralCount}</p>
                    </div>
                </div>

                <div className="channel-info-container">
                    {channelLogo ? (
                        <img src={channelLogo} alt="Channel Logo" className="channel-logo" />
                    ) : (
                        <p className="error-text">No Channel Logo</p>
                    )}
                    {videoTitle ? (
                        <p className="video-title">{videoTitle}</p>
                    ) : (
                        <p className="error-text">No Video Title</p>
                    )}
                </div>
            </div>

            <div className="chat-container">
                <h1>Live Chat Sentiment Analysis</h1>
                <div className="chat-box">
                    {data.length > 0 ? (
                        data.map((chat) => (
                            <div key={`${chat.published_at}-${chat.author}`} className={`chat-message ${chat.final_sentiment}`}>
                                <strong>{new Date(chat.published_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })} <span className="author">{chat.author}:</span></strong> {chat.message}
                            </div>
                        ))
                    ) : (
                        <p className="loading">Loading chat...</p>
                    )}
                    <div ref={chatEndRef}></div>
                </div>
            </div>

            <div className="charts-wrapper">
                <div className="chart-container">
                    <PieChart width={415} height={220}>
                        <Pie
                            data={sentimentData}
                            cx="55%"
                            cy="50%"
                            innerRadius={40}
                            outerRadius={85}
                            paddingAngle={3}
                            dataKey="value"
                            label={({ name, percent }) => `${name} ${percent ? (percent * 100).toFixed(1) : 0}%`}
                        >
                            {sentimentData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Pie>
                        <Tooltip />
                    </PieChart>
                </div>

                <div className="chart-container">
                    <BarChart width={415} height={220} data={sentimentBarData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="value" fill="#8884d8" barSize={50} />
                    </BarChart>
                </div>

                <div className="chart-container">
                    <LineChart width={415} height={220} data={sentimentOverTime}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="time" interval="preserveStartEnd" />
                        <YAxis domain={[-1, 1]} tickCount={3} />
                        <Tooltip />
                        <Line type="monotone" dataKey="sentiment" stroke="#82ca9d" strokeWidth={2} dot={false} />
                    </LineChart>
                </div>
            </div>
        </div>
    );
}

export default App;
