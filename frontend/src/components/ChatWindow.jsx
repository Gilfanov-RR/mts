import React, {useState, useEffect} from "react";
import axios from "axios";
import ModelPanel from "./ModelPanel";
import FileUploader from "./FileUploader";
import VoiceRecorder from "./VoiceRecorder";

export default function ChatWindow({userId}) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [model, setModel] = useState(null);

  const send = async () => {
    const payload = {text: input, model, user_id: userId};
    const r = await axios.post("/api/chat", payload);
    setMessages([...messages, {from: "user", text: input}, {from: "bot", text: r.data.answer, meta: r.data.meta}]);
    setInput("");
  };

  return (
    <div className="chat">
      <div className="messages">
        {messages.map((m,i) => <div key={i} className={m.from}>{m.text}<pre>{JSON.stringify(m.meta || {}, null, 2)}</pre></div>)}
      </div>
      <ModelPanel onSelect={setModel} selected={model}/>
      <FileUploader onUpload={(file)=>{/* upload to /api/upload */}}/>
      <VoiceRecorder onTranscribed={(text)=> setInput(text)}/>
      <textarea value={input} onChange={e=>setInput(e.target.value)} />
      <button onClick={send}>Send</button>
    </div>
  );
}
