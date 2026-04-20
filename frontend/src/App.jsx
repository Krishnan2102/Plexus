import React, { useEffect, useState, useRef } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import axios from 'axios';
import SpriteText from 'three-spritetext';

const App = () => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState([{ role: "ai", text: "Plexus Online. How can I assist your intelligence search?" }]);
  const [loading, setLoading] = useState(false);

  // Fetch initial graph data
  useEffect(() => {
    axios.get('http://localhost:8000/graph').then(res => {
      const nodes = []; const links = []; const nodeIds = new Set();
      res.data.data.forEach(item => {
        if (!nodeIds.has(item.source.id)) {
          nodes.push({ id: item.source.id, name: item.source.name, label: item.source.label });
          nodeIds.add(item.source.id);
        }
        if (!nodeIds.has(item.target.id)) {
          nodes.push({ id: item.target.id, name: item.target.name, label: item.target.label });
          nodeIds.add(item.target.id);
        }
        links.push({ source: item.source.id, target: item.target.id, relationship: item.relationship });
      });
      setGraphData({ nodes, links });
    });
  }, []);

  const handleSendMessage = async () => {
    if (!chatInput.trim()) return;
    const userMsg = chatInput;
    setMessages(prev => [...prev, { role: "user", text: userMsg }]);
    setChatInput("");
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/chat', { message: userMsg });
      setMessages(prev => [...prev, { role: "ai", text: response.data.answer }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: "ai", text: "Error: Could not reach the backend." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#000', position: 'relative' }}>
      
      {/* 3D GRAPH LAYER */}
      <ForceGraph3D
        graphData={graphData}
        nodeAutoColorBy="label"
        nodeThreeObject={node => {
          const sprite = new SpriteText(node.name);
          sprite.color = '#ffffff';
          sprite.textHeight = 6;
          return sprite;
        }}
        nodeThreeObjectExtend={true}
        linkDirectionalArrowLength={3.5}
        linkDirectionalArrowRelPos={1}
        linkColor={() => 'rgba(0, 242, 255, 0.2)'}
      />

      {/* FLOATING CHAT SIDEBAR */}
      <div style={{
        position: 'absolute', top: '20px', right: '20px', bottom: '20px',
        width: '350px', background: 'rgba(15, 15, 15, 0.85)',
        backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: '12px', display: 'flex', flexDirection: 'column',
        zIndex: 100, color: 'white', fontFamily: 'Inter, sans-serif'
      }}>
        <div style={{ padding: '20px', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
          <h2 style={{ margin: 0, fontSize: '18px', color: '#00f2ff' }}>PLEXUS CHAT</h2>
        </div>

        <div style={{ flex: 1, overflowY: 'auto', padding: '20px', display: 'flex', flexDirection: 'column', gap: '15px' }}>
          {messages.map((msg, i) => (
            <div key={i} style={{
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              background: msg.role === 'user' ? '#00f2ff22' : 'rgba(255,255,255,0.05)',
              padding: '10px 15px', borderRadius: '10px', maxWidth: '85%', fontSize: '14px'
            }}>
              {msg.text}
            </div>
          ))}
          {loading && <div style={{ fontSize: '12px', opacity: 0.5 }}>Plexus is analyzing the graph...</div>}
        </div>

        <div style={{ padding: '20px', borderTop: '1px solid rgba(255,255,255,0.1)', display: 'flex', gap: '10px' }}>
          <input 
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask about connections..."
            style={{ 
              flex: 1, background: '#000', border: '1px solid #333', 
              borderRadius: '6px', color: '#fff', padding: '8px 12px', outline: 'none'
            }}
          />
          <button onClick={handleSendMessage} style={{ 
            background: '#00f2ff', color: '#000', border: 'none', 
            borderRadius: '6px', padding: '8px 15px', fontWeight: 'bold', cursor: 'pointer'
          }}>SEND</button>
        </div>
      </div>
    </div>
  );
};

export default App;