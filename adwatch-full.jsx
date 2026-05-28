import { useState, useEffect, useRef } from "react";

// ═════════════════════════════════════════════════════════════
// DESIGN TOKENS
// ═════════════════════════════════════════════════════════════
const C = {
  bg: "#07070f",
  surface: "#0e0e1c",
  card: "#151528",
  cardHover: "#1c1c35",
  border: "#ffffff0d",
  accent: "#ffcc00",
  accentDim: "#ffcc0015",
  accentGlow: "#ffcc0040",
  green: "#00f080",
  greenDim: "#00f08015",
  purple: "#a855f7",
  purpleDim: "#a855f715",
  text: "#ede9e3",
  muted: "#64637a",
};

const GLOBAL_CSS = `
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Outfit:wght@300;400;500;600&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: ${C.bg}; color: ${C.text}; font-family: 'Outfit', sans-serif; -webkit-font-smoothing: antialiased; }
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-thumb { background: ${C.border}; border-radius: 99px; }

@keyframes fadeUp { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@keyframes pulse { 0%,100% { opacity:1; transform:scale(1); } 50% { opacity:0.7; } }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes glow { 0%,100% { box-shadow: 0 0 20px ${C.accentGlow}; } 50% { box-shadow: 0 0 50px ${C.accentGlow}; } }
@keyframes pop { 0% { transform:scale(0.5); opacity:0; } 100% { transform:scale(1); opacity:1; } }

.fu { animation: fadeUp 0.5s ease both; }
.fu1 { animation: fadeUp 0.5s 0.08s ease both; }
.fu2 { animation: fadeUp 0.5s 0.16s ease both; }
.fu3 { animation: fadeUp 0.5s 0.24s ease both; }
`;

// ═════════════════════════════════════════════════════════════
// DATA
// ═════════════════════════════════════════════════════════════
const ADS = [
  { id:1, brand:"Nike",      category:"Sports",     reward:0.45, duration:10, color:"#ff6b35", bg:"#1a0d08", emoji:"👟", tagline:"Just Do It" },
  { id:2, brand:"Spotify",   category:"Music",      reward:0.30, duration:8,  color:"#1db954", bg:"#081209", emoji:"🎵", tagline:"Music for everyone" },
  { id:3, brand:"Airbnb",    category:"Travel",     reward:0.60, duration:12, color:"#ff5a5f", bg:"#1a0809", emoji:"🏠", tagline:"Belong anywhere" },
  { id:4, brand:"Samsung",   category:"Tech",       reward:0.50, duration:10, color:"#5bb8f5", bg:"#080f1a", emoji:"📱", tagline:"Do Bigger" },
  { id:5, brand:"Coca-Cola", category:"Food",       reward:0.25, duration:6,  color:"#f40000", bg:"#1a0808", emoji:"🥤", tagline:"Open Happiness" },
  { id:6, brand:"Apple",     category:"Tech",       reward:0.70, duration:15, color:"#e0e0e0", bg:"#111111", emoji:"🍎", tagline:"Think Different" },
  { id:7, brand:"Netflix",   category:"Streaming",  reward:0.55, duration:12, color:"#e50914", bg:"#1a0808", emoji:"🎬", tagline:"See what's next" },
  { id:8, brand:"Adidas",    category:"Sports",     reward:0.40, duration:10, color:"#ffffff", bg:"#111111", emoji:"⚡", tagline:"Impossible" },
];

const LEADERBOARD = [
  { rank:1, name:"QuantumEarner",  earned:284.50, badge:"🏆" },
  { rank:2, name:"CashKing99",     earned:231.20, badge:"🥈" },
  { rank:3, name:"AdWatcher_Pro",  earned:198.75, badge:"🥉" },
  { rank:4, name:"MoneyMoves",     earned:167.40 },
  { rank:5, name:"EarnDaily",      earned:145.90 },
  { rank:6, name:"PocketFuel",     earned:128.60 },
  { rank:7, name:"WatchNWin",      earned:112.30 },
  { rank:8, name:"GrindAndGain",   earned:98.70 },
  { rank:9, name:"DailyHustle",    earned:87.20 },
  { rank:10,name:"QuickCash2024",  earned:74.50 },
];

// ═════════════════════════════════════════════════════════════
// ICONS
// ═════════════════════════════════════════════════════════════
const Icon = ({ n, size=20, color="currentColor" }) => {
  const p = {
    play:    <polygon points="5,3 19,12 5,21" fill={color}/>,
    earn:    <circle cx="12" cy="12" r="9" fill="none" stroke={color} strokeWidth="2"/>,
    wallet:  <><rect x="2" y="6" width="20" height="14" rx="2" fill="none" stroke={color} strokeWidth="2"/><path d="M2 10h20" stroke={color} strokeWidth="2"/></>,
    users:   <><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" fill="none" stroke={color} strokeWidth="2"/><circle cx="9" cy="7" r="4" fill="none" stroke={color} strokeWidth="2"/></>,
    trophy:  <><path d="M6 9H4.5a2.5 2.5 0 0 0 0 5H6" fill="none" stroke={color} strokeWidth="2"/><path d="M18 9h1.5a2.5 2.5 0 0 1 0 5H18" fill="none" stroke={color} strokeWidth="2"/><path d="M4 22h16M12 17v5M8 17h8" fill="none" stroke={color} strokeWidth="2"/></>,
    copy:    <><rect x="9" y="9" width="13" height="13" rx="2" fill="none" stroke={color} strokeWidth="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" fill="none" stroke={color} strokeWidth="2"/></>,
    check:   <><circle cx="12" cy="12" r="10" fill={color} opacity="0.2"/><polyline points="9,12 11,14 15,10" fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round"/></>,
    bolt:    <polygon points="13,2 3,14 12,14 11,22 21,10 12,10" fill={color}/>,
    gift:    <><rect x="3" y="8" width="18" height="13" rx="2" fill="none" stroke={color} strokeWidth="2"/><path d="M12 8V21M3 13h18" fill="none" stroke={color} strokeWidth="2"/></>,
    logout:  <><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" fill="none" stroke={color} strokeWidth="2"/><polyline points="16,17 21,12 16,7" fill="none" stroke={color} strokeWidth="2"/></>,
    ai:      <circle cx="12" cy="12" r="3" fill={color}/>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">{p[n]}</svg>;
};

const Avatar = ({ name, size=36 }) => {
  const initials = name.split(" ").map(w=>w[0]).join("").slice(0,2).toUpperCase();
  const hue = name.charCodeAt(0) * 137 % 360;
  return <div style={{ width:size, height:size, borderRadius:"50%", background:`hsl(${hue},60%,35%)`, display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"Syne, sans-serif", fontWeight:700, fontSize:size/2.5, color:"white" }}>{initials}</div>;
};

const genRefCode = (name) => {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  let code = name.replace(/[^a-zA-Z]/g,"").slice(0,3).toUpperCase();
  let seed = name.split("").reduce((a,c)=>a+c.charCodeAt(0),0);
  for(let i=0;i<4;i++){ code += chars[(seed*31+i*7)%chars.length]; }
  return code;
};

const Spinner = ({ size=20 }) => <div style={{ width:size, height:size, border:`2px solid ${C.accent}30`, borderTop:`2px solid ${C.accent}`, borderRadius:"50%", animation:"spin 0.8s linear infinite" }}/>;

// ═════════════════════════════════════════════════════════════
// AUTH SCREEN
// ═════════════════════════════════════════════════════════════
const AuthScreen = ({ onAuth }) => {
  const [mode, setMode] = useState("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);

  const handle = () => {
    setErr("");
    if(mode==="signup" && !name.trim()){ setErr("Name is required"); return; }
    if(!email.includes("@")){ setErr("Valid email needed"); return; }
    if(pass.length < 6){ setErr("Password 6+ chars"); return; }
    setLoading(true);
    setTimeout(() => {
      const userName = mode==="signup" ? name.trim() : email.split("@")[0];
      onAuth({ name: userName, email, referralCode: genRefCode(userName), isNew: mode==="signup" });
    }, 900);
  };

  const inp = (val, setVal, placeholder, type="text") => (
    <input type={type} value={val} placeholder={placeholder} onChange={e=>setVal(e.target.value)} onKeyDown={e=>e.key==="Enter"&&handle()}
      style={{ width:"100%", background:C.card, border:`1px solid ${C.border}`, borderRadius:12, padding:"14px 16px", color:C.text, fontSize:15, outline:"none" }}
      onFocus={e=>e.target.style.borderColor=C.accent+"66"} onBlur={e=>e.target.style.borderColor=C.border}/>
  );

  return (
    <div style={{ minHeight:"100vh", background:C.bg, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:24 }}>
      <style>{GLOBAL_CSS}</style>
      <div className="fu" style={{ textAlign:"center", marginBottom:40 }}>
        <div style={{ fontFamily:"Syne, sans-serif", fontSize:36, fontWeight:800, color:C.accent }}>AdWatch<span style={{color:C.green}}>.</span></div>
        <div style={{ color:C.muted, fontSize:14, marginTop:4 }}>Watch ads. Earn real money.</div>
      </div>

      <div className="fu1" style={{ width:"100%", maxWidth:380, background:C.surface, border:`1px solid ${C.border}`, borderRadius:24, padding:32 }}>
        <div style={{ display:"flex", background:C.card, borderRadius:12, padding:4, marginBottom:28 }}>
          {["login","signup"].map(m=><button key={m} onClick={()=>setMode(m)} style={{ flex:1, padding:"10px", borderRadius:9, border:"none", background:mode===m?C.accent:"transparent", color:mode===m?"#000":C.muted, fontWeight:600, fontSize:14, cursor:"pointer" }}>{m==="login"?"Sign In":"Sign Up"}</button>)}
        </div>

        <div style={{ display:"flex", flexDirection:"column", gap:12 }}>
          {mode==="signup" && inp(name, setName, "Your name")}
          {inp(email, setEmail, "Email", "email")}
          {inp(pass, setPass, "Password", "password")}
        </div>

        {err && <div style={{ color:"#ff5f6d", fontSize:13, marginTop:10, textAlign:"center" }}>{err}</div>}

        <button onClick={handle} style={{ width:"100%", marginTop:20, padding:"16px", background:C.accent, color:"#000", fontWeight:700, fontSize:16, borderRadius:100, border:"none", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center", gap:8, animation:"glow 3s ease-in-out infinite" }}>
          {loading ? <Spinner size={18}/> : (mode==="signup" ? "Create Account →" : "Sign In →")}
        </button>
      </div>
    </div>
  );
};

// ═════════════════════════════════════════════════════════════
// AD PLAYER
// ═════════════════════════════════════════════════════════════
const AdPlayer = ({ ad, onComplete, onSkip }) => {
  const [progress, setProgress] = useState(0);
  const [canSkip, setCanSkip] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const ref = useRef(null);

  useEffect(()=>{
    let e = 0;
    ref.current = setInterval(()=>{ e += 0.1; setElapsed(Math.floor(e)); setProgress(Math.min((e/ad.duration)*100,100)); if(e>=5) setCanSkip(true); if(e>=ad.duration){ clearInterval(ref.current); onComplete(ad); } },100);
    return ()=>clearInterval(ref.current);
  },[]);

  return (
    <div style={{ position:"fixed", inset:0, background:ad.bg, display:"flex", flexDirection:"column", zIndex:100 }}>
      <div style={{ display:"flex", justifyContent:"space-between", padding:"20px 24px" }}>
        <div style={{ fontSize:11, color:"rgba(255,255,255,0.4)" }}>Advertisement</div>
        {canSkip ? <button onClick={onSkip} style={{ background:"rgba(255,255,255,0.1)", border:"1px solid rgba(255,255,255,0.2)", color:"rgba(255,255,255,0.8)", borderRadius:100, padding:"6px 16px", fontSize:12, cursor:"pointer" }}>Skip ✕</button> : <div style={{ fontSize:12, color:"rgba(255,255,255,0.4)" }}>Skip in {Math.max(0,5-elapsed)}s</div>}
      </div>

      <div style={{ flex:1, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", gap:16 }}>
        <div style={{ fontSize:80 }}>{ad.emoji}</div>
        <div style={{ fontFamily:"Syne, sans-serif", fontSize:64, fontWeight:800, color:ad.color, textShadow:`0 0 80px ${ad.color}66` }}>{ad.brand.toUpperCase()}</div>
        <div style={{ color:"rgba(255,255,255,0.4)", fontSize:16 }}>{ad.tagline}</div>
        <div style={{ width:300, height:160, background:`${ad.color}11`, border:`1px solid ${ad.color}30`, borderRadius:20, display:"flex", alignItems:"center", justifyContent:"center" }}>
          <div style={{ width:56, height:56, borderRadius:"50%", background:`${ad.color}25`, border:`2px solid ${ad.color}`, display:"flex", alignItems:"center", justifyContent:"center", animation:"pulse 2s ease-in-out infinite" }}>
            <Icon n="play" color={ad.color} size={24}/>
          </div>
        </div>
      </div>

      <div style={{ padding:"0 24px 40px" }}>
        <div style={{ display:"flex", justifyContent:"space-between", marginBottom:10, fontSize:12 }}>
          <span style={{ color:"rgba(255,255,255,0.4)" }}>{elapsed}s / {ad.duration}s</span>
          <span style={{ color:C.green, fontWeight:700, fontSize:18 }}>+${ad.reward.toFixed(2)}</span>
        </div>
        <div style={{ background:"rgba(255,255,255,0.08)", borderRadius:99, height:6 }}>
          <div style={{ height:"100%", width:`${progress}%`, background:`linear-gradient(90deg,${ad.color},${C.green})`, borderRadius:99, transition:"width 0.1s" }}/>
        </div>
      </div>
    </div>
  );
};

// ═════════════════════════════════════════════════════════════
// AD COMPLETE
// ═════════════════════════════════════════════════════════════
const AdComplete = ({ ad, balance, onContinue, onWallet }) => (
  <div style={{ minHeight:"100vh", background:C.bg, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", textAlign:"center" }}>
    <div style={{ width:100, height:100, borderRadius:"50%", background:C.greenDim, border:`2px solid ${C.green}`, display:"flex", alignItems:"center", justifyContent:"center", marginBottom:24, animation:"pop 0.5s ease" }}>
      <Icon n="check" color={C.green} size={50}/>
    </div>
    <div style={{ fontSize:13, color:C.green, textTransform:"uppercase", letterSpacing:2, marginBottom:12 }}>Earned!</div>
    <div style={{ fontFamily:"Syne, sans-serif", fontSize:72, fontWeight:800, color:C.accent }}>+${ad.reward.toFixed(2)}</div>
    <div style={{ color:C.muted, fontSize:15, margin:"20px 0 8px" }}>from {ad.brand}</div>
    <div style={{ color:C.muted, fontSize:14, marginBottom:40 }}>Balance: <strong style={{color:C.text}}>${balance.toFixed(2)}</strong></div>
    <div style={{ display:"flex", flexDirection:"column", gap:12, width:"100%", maxWidth:280 }}>
      <button onClick={onContinue} style={{ padding:"16px", background:C.accent, color:"#000", fontWeight:700, fontSize:16, borderRadius:100, border:"none", cursor:"pointer" }}>Watch Another →</button>
      <button onClick={onWallet} style={{ padding:"16px", background:"transparent", color:C.text, border:`1px solid ${C.border}`, borderRadius:100, cursor:"pointer" }}>View Wallet</button>
    </div>
  </div>
);

// ═════════════════════════════════════════════════════════════
// TABS
// ═════════════════════════════════════════════════════════════
const EarnTab = ({ watchHistory, balance, watched, onWatch }) => {
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetched, setFetched] = useState(false);

  const getAIRecs = async () => {
    setLoading(true);
    try {
      const watchedCats = watchHistory.map(id=>ADS.find(a=>a.id===id)?.category).filter(Boolean);
      const res = await fetch("https://api.anthropic.com/v1/messages",{
        method:"POST", headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
          model:"claude-sonnet-4-20250514", max_tokens:400,
          messages:[{ role:"user", content:`Recommend 3 ads from: ${JSON.stringify(ADS.map(a=>({id:a.id,brand:a.brand,category:a.category,reward:a.reward})))} for user who watches: [${watchedCats.join(",")||"none"}]. Reply ONLY with JSON array (no markdown): [{"id":1,"reason":"text"},...]` }]
        })
      });
      const d = await res.json();
      const txt = d.content.map(i=>i.text||"").join("").replace(/```json|```/g,"").trim();
      setRecs(JSON.parse(txt));
      setFetched(true);
    } catch(e) {}
    setLoading(false);
  };

  return (
    <div style={{ overflowY:"auto", flex:1 }}>
      <div className="fu" style={{ margin:16, background:`linear-gradient(135deg,${C.card},#1c1c38)`, border:`1px solid ${C.accent}22`, borderRadius:24, padding:"24px 20px" }}>
        <div style={{ fontSize:11, color:C.muted }}>TOTAL BALANCE</div>
        <div style={{ fontFamily:"Syne, sans-serif", fontSize:48, fontWeight:800, color:C.accent, margin:"6px 0" }}>${balance.toFixed(2)}</div>
        <div style={{ display:"flex", gap:24 }}>
          <div><div style={{fontSize:10,color:C.muted}}>ADS WATCHED</div><div style={{fontWeight:600,fontSize:18}}>{watched}</div></div>
          <div><div style={{fontSize:10,color:C.muted}}>TODAY</div><div style={{fontWeight:600,color:C.green,fontSize:18}}>+${(watched*0.3).toFixed(2)}</div></div>
        </div>
      </div>

      <div className="fu1" style={{ margin:"0 16px 16px" }}>
        <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:10 }}>
          <div style={{ display:"flex", alignItems:"center", gap:6 }}>
            <Icon n="ai" color={C.purple} size={16}/>
            <span style={{ fontSize:12, color:C.purple, fontWeight:600 }}>AI PICKS</span>
          </div>
          <button onClick={getAIRecs} disabled={loading} style={{ background:C.purpleDim, border:`1px solid ${C.purple}44`, borderRadius:100, padding:"6px 14px", fontSize:12, color:C.purple, fontWeight:600, cursor:"pointer", display:"flex", alignItems:"center", gap:6 }}>
            {loading ? <><Spinner size={12}/> Thinking...</> : "Get Recommendations"}
          </button>
        </div>

        {fetched && recs.length>0 && recs.map((r,i)=>{
          const ad = ADS.find(a=>a.id===r.id);
          return ad ? (
            <div key={i} onClick={()=>onWatch(ad)} style={{ background:`linear-gradient(135deg,${C.purple}15,${C.card})`, border:`1px solid ${C.purple}33`, borderRadius:14, padding:"14px 16px", display:"flex", alignItems:"center", gap:12, cursor:"pointer", marginBottom:8 }}>
              <div style={{ fontSize:28 }}>{ad.emoji}</div>
              <div style={{ flex:1 }}>
                <div style={{ fontWeight:600 }}>{ad.brand} <span style={{color:C.purple,fontSize:11}}>★ AI</span></div>
                <div style={{ color:C.muted, fontSize:12 }}>{r.reason}</div>
              </div>
              <div style={{ color:C.green, fontWeight:700 }}>+${ad.reward.toFixed(2)}</div>
            </div>
          ) : null;
        })}

        {!fetched && !loading && <div style={{ background:C.purpleDim, border:`1px dashed ${C.purple}33`, borderRadius:14, padding:16, textAlign:"center", fontSize:13, color:C.muted }}>Let AI recommend the best ads for you.</div>}
      </div>

      <div style={{ margin:"0 16px" }}>
        <div style={{ fontSize:11, color:C.muted, marginBottom:10 }}>ALL ADS</div>
        <div style={{ display:"flex", flexDirection:"column", gap:10 }}>
          {ADS.map(ad=>(
            <div key={ad.id} onClick={()=>onWatch(ad)} style={{ background:C.card, border:`1px solid ${C.border}`, borderRadius:16, padding:"16px", display:"flex", alignItems:"center", gap:14, cursor:"pointer" }}>
              <div style={{ width:44, height:44, borderRadius:12, background:ad.bg, border:`1px solid ${ad.color}33`, display:"flex", alignItems:"center", justifyContent:"center", fontSize:22 }}>{ad.emoji}</div>
              <div style={{ flex:1 }}>
                <div style={{ fontWeight:600 }}>{ad.brand}</div>
                <div style={{ color:C.muted, fontSize:12 }}>{ad.category} · {ad.duration}s</div>
              </div>
              <div style={{ textAlign:"right" }}>
                <div style={{ color:C.green, fontWeight:700, fontSize:16 }}>+${ad.reward.toFixed(2)}</div>
                <div style={{ fontSize:11, color:C.muted }}>▶ watch</div>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div style={{ height:24 }}/>
    </div>
  );
};

const WalletTab = ({ balance, coins, transactions }) => {
  const [withdrawn, setWithdrawn] = useState(false);

  return (
    <div style={{ overflowY:"auto", flex:1, padding:"16px 16px 24px" }}>
      <div className="fu" style={{ background:`linear-gradient(135deg,#1a1a30,#0f0f20)`, border:`1px solid ${C.accent}22`, borderRadius:24, padding:"28px 24px", marginBottom:20, textAlign:"center" }}>
        <div style={{ fontSize:12, color:C.muted }}>AVAILABLE BALANCE</div>
        <div style={{ fontFamily:"Syne, sans-serif", fontSize:56, fontWeight:800, color:C.accent }}>${balance.toFixed(2)}</div>
        <div style={{ color:C.muted, fontSize:13 }}>≈ {coins} coins</div>
        {balance < 5 && <div style={{ marginTop:12, fontSize:12, color:C.muted }}>Min $5 to withdraw · ${(5-balance).toFixed(2)} more needed</div>}
      </div>

      <div style={{ fontSize:11, color:C.muted, marginBottom:12 }}>WITHDRAW TO</div>
      {[
        { label:"PayPal Cash",       min:5,   emoji:"💸", color:C.accent },
        { label:"Amazon Gift Card",  min:10,  emoji:"🎁", color:C.green },
        { label:"Crypto (BTC/ETH)",  min:25,  emoji:"₿",  color:"#f7931a" },
      ].map((m,i)=>{
        const ok = balance >= m.min;
        return (
          <div key={i} onClick={()=>{ if(ok && !withdrawn){ setWithdrawn(true); setTimeout(()=>setWithdrawn(false),3000); } }} style={{ background:C.card, border:`1px solid ${ok?C.border:C.border+"80"}`, borderRadius:16, padding:"16px", marginBottom:10, display:"flex", alignItems:"center", gap:14, cursor:ok?"pointer":"default", opacity:ok?1:0.45 }}>
            <div style={{ fontSize:28 }}>{m.emoji}</div>
            <div style={{ flex:1 }}>
              <div style={{ fontWeight:600 }}>{m.label}</div>
              <div style={{ color:C.muted, fontSize:12 }}>Min. ${m.min.toFixed(2)}</div>
            </div>
            <div style={{ color:ok?m.color:C.muted, fontSize:12, fontWeight:600 }}>{withdrawn && ok?"✓ Requested":ok?"Withdraw":"Locked"}</div>
          </div>
        );
      })}

      {withdrawn && <div style={{ background:C.greenDim, border:`1px solid ${C.green}44`, borderRadius:12, padding:14, textAlign:"center", fontSize:13, color:C.green, marginTop:4 }}>✅ Requested! 1–3 business days.</div>}

      <div style={{ marginTop:24 }}>
        <div style={{ fontSize:11, color:C.muted, marginBottom:12 }}>HISTORY</div>
        {transactions.map((t,i)=>(
          <div key={i} style={{ display:"flex", justifyContent:"space-between", padding:"14px 0", borderBottom:`1px solid ${C.border}` }}>
            <div>
              <div style={{ fontSize:14, fontWeight:500 }}>{t.label}</div>
              <div style={{ fontSize:11, color:C.muted }}>{t.time}</div>
            </div>
            <div style={{ color:t.amount>0?C.green:C.red, fontWeight:700 }}>{t.amount>0?"+":""}{t.amount.toFixed(2)}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

const ReferralTab = ({ user }) => {
  const [copied, setCopied] = useState(false);
  const link = `https://adwatch.app/ref/${user.referralCode}`;

  const copy = () => {
    navigator.clipboard?.writeText(link).catch(()=>{});
    setCopied(true);
    setTimeout(()=>setCopied(false), 2000);
  };

  return (
    <div style={{ overflowY:"auto", flex:1, padding:"16px 16px 24px" }}>
      <div className="fu" style={{ background:`linear-gradient(135deg,${C.green}18,${C.card})`, border:`1px solid ${C.green}22`, borderRadius:24, padding:"24px 20px", marginBottom:20, textAlign:"center" }}>
        <div style={{ fontSize:40, marginBottom:8 }}>🤝</div>
        <div style={{ fontFamily:"Syne, sans-serif", fontSize:28, fontWeight:800 }}>Invite & Earn</div>
        <div style={{ color:C.muted, fontSize:14, marginTop:4 }}>Get <strong style={{color:C.green}}>$0.50</strong> per friend</div>
        <div style={{ display:"flex", gap:24, justifyContent:"center", marginTop:16 }}>
          <div><div style={{fontSize:28,fontWeight:800,color:C.green}}>2</div><div style={{fontSize:12,color:C.muted}}>referrals</div></div>
          <div style={{width:1,background:C.border}}/>
          <div><div style={{fontSize:28,fontWeight:800,color:C.accent}}>$1.00</div><div style={{fontSize:12,color:C.muted}}>earned</div></div>
        </div>
      </div>

      <div className="fu1" style={{ marginBottom:16 }}>
        <div style={{ fontSize:11, color:C.muted, marginBottom:10 }}>YOUR LINK</div>
        <div style={{ background:C.card, border:`1px solid ${C.border}`, borderRadius:14, padding:"14px 16px", display:"flex", alignItems:"center", gap:10 }}>
          <div style={{ flex:1, fontFamily:"monospace", fontSize:12, color:C.accent, overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap" }}>{link}</div>
          <button onClick={copy} style={{ background:copied?C.greenDim:C.accentDim, border:`1px solid ${copied?C.green+"44":C.accent+"44"}`, borderRadius:8, padding:"8px 14px", fontSize:12, color:copied?C.green:C.accent, cursor:"pointer", fontWeight:600 }}>
            <Icon n={copied?"check":"copy"} size={12}/>
          </button>
        </div>
      </div>

      <div className="fu2" style={{ marginBottom:20 }}>
        <div style={{ fontSize:11, color:C.muted, marginBottom:10 }}>REWARD TIERS</div>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:10 }}>
          {[
            { label:"Starter",  count:"1+",  bonus:"$0.50/ref" },
            { label:"Grower",   count:"5+",  bonus:"$0.75/ref" },
            { label:"Builder",  count:"10+", bonus:"$1.00/ref" },
            { label:"Pro",      count:"25+", bonus:"$1.50/ref" },
          ].map((t,i)=>(
            <div key={i} style={{ background:i<1?C.greenDim:C.card, border:`1px solid ${i<1?C.green+"44":C.border}`, borderRadius:14, padding:16, textAlign:"center" }}>
              <div style={{ fontSize:11, color:i<1?C.green:C.muted, fontWeight:600 }}>{t.label}</div>
              <div style={{ fontWeight:700, fontSize:16, margin:"6px 0 2px" }}>{t.bonus}</div>
              <div style={{ fontSize:11, color:C.muted }}>{t.count} {i<1?"✓":""}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="fu3">
        <div style={{ fontSize:11, color:C.muted, marginBottom:10 }}>YOUR REFERRALS</div>
        {[{ name:"Alex M.",  joined:"2d ago" }, { name:"Priya K.", joined:"5d ago" }].map((r,i)=>(
          <div key={i} style={{ display:"flex", alignItems:"center", gap:12, padding:"14px 0", borderBottom:`1px solid ${C.border}` }}>
            <Avatar name={r.name} size={38}/>
            <div style={{ flex:1 }}>
              <div style={{ fontWeight:500 }}>{r.name}</div>
              <div style={{ fontSize:11, color:C.muted }}>Joined {r.joined}</div>
            </div>
            <div style={{ color:C.green, fontWeight:700 }}>+$0.50</div>
          </div>
        ))}
      </div>
    </div>
  );
};

const LeaderboardTab = ({ user, balance }) => {
  return (
    <div style={{ overflowY:"auto", flex:1, padding:"16px 16px 24px" }}>
      <div className="fu" style={{ textAlign:"center", marginBottom:24 }}>
        <div style={{ fontFamily:"Syne, sans-serif", fontSize:28, fontWeight:800 }}>Top Earners</div>
        <div style={{ color:C.muted, fontSize:13, marginTop:4 }}>This Month</div>
      </div>

      <div className="fu1" style={{ display:"flex", gap:8, alignItems:"flex-end", justifyContent:"center", marginBottom:24 }}>
        {[LEADERBOARD[1],LEADERBOARD[0],LEADERBOARD[2]].map((u,i)=>{
          const heights = [100,130,85];
          const colors = [C.muted,C.accent,"#cd7f32"];
          const labels = ["2nd","1st","3rd"];
          return (
            <div key={i} style={{ flex:1, display:"flex", flexDirection:"column", alignItems:"center", gap:8 }}>
              <Avatar name={u.name} size={i===1?48:38}/>
              <div style={{ fontSize:11, color:C.muted }}>{u.name.slice(0,10)}</div>
              <div style={{ width:"100%", height:heights[i], background:`${colors[i]}22`, border:`1px solid ${colors[i]}44`, borderRadius:"8px 8px 0 0", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center" }}>
                <div style={{ fontWeight:800, color:colors[i], fontSize:i===1?20:16 }}>{labels[i]}</div>
                <div style={{ fontSize:11, color:C.muted }}>${u.earned.toFixed(0)}</div>
              </div>
            </div>
          );
        })}
      </div>

      {LEADERBOARD.map((u,i)=>(
        <div key={i} style={{ display:"flex", alignItems:"center", gap:12, padding:"13px 14px", borderRadius:14, marginBottom:6, background:i<3?C.card:"transparent", border:`1px solid ${i<3?C.border:"transparent"}` }}>
          <div style={{ width:28, textAlign:"center", fontWeight:700, fontSize:15, color:i===0?C.accent:i===1?C.muted:i===2?"#cd7f32":C.muted }}>{u.rank}</div>
          <Avatar name={u.name} size={34}/>
          <div style={{ flex:1 }}>
            <div style={{ fontWeight:600 }}>{u.name}</div>
          </div>
          <div style={{ textAlign:"right" }}>
            <div style={{ fontWeight:700, color:i===0?C.accent:C.text }}>${u.earned.toFixed(2)}</div>
            <div style={{ fontSize:10, color:C.muted }}>this month</div>
          </div>
          <div style={{ fontSize:16 }}>{u.badge||"⭐"}</div>
        </div>
      ))}
    </div>
  );
};

// ═════════════════════════════════════════════════════════════
// MAIN APP
// ═════════════════════════════════════════════════════════════
const MainApp = ({ user, onLogout }) => {
  const [tab, setTab] = useState("earn");
  const [watching, setWatching] = useState(null);
  const [completed, setCompleted] = useState(null);
  const [balance, setBalance] = useState(user.isNew ? 1.00 : 3.80);
  const [coins, setCoins] = useState(user.isNew ? 100 : 380);
  const [watched, setWatched] = useState(user.isNew ? 0 : 7);
  const [watchHistory, setWatchHistory] = useState([]);
  const [trans, setTrans] = useState(user.isNew ? [{ label:"Welcome Bonus 🎁", amount:1.00, time:"Just now" }] : [{ label:"Nike ad", amount:0.45, time:"2m ago" }]);

  const tabs = [
    { key:"earn", icon:"earn", label:"Earn" },
    { key:"wallet", icon:"wallet", label:"Wallet" },
    { key:"referrals", icon:"users", label:"Refer" },
    { key:"leaderboard", icon:"trophy", label:"Ranks" },
  ];

  const handleComplete = (ad) => {
    setWatching(null);
    setCompleted(ad);
    setBalance(b => Math.round((b + ad.reward)*100)/100);
    setCoins(c => c + Math.round(ad.reward*100));
    setWatched(w => w+1);
    setWatchHistory(h => [ad.id, ...h]);
    setTrans(t => [{ label:`${ad.brand} ad watched`, amount:ad.reward, time:"Just now" }, ...t]);
  };

  if(watching) return <AdPlayer ad={watching} onComplete={handleComplete} onSkip={()=>setWatching(null)}/>;
  if(completed) return <AdComplete ad={completed} balance={balance} onContinue={()=>setCompleted(null)} onWallet={()=>{setCompleted(null);setTab("wallet");}}/>;

  return (
    <div style={{ height:"100vh", display:"flex", flexDirection:"column", background:C.bg }}>
      <style>{GLOBAL_CSS}</style>
      <div style={{ background:C.surface, borderBottom:`1px solid ${C.border}`, padding:"14px 20px", display:"flex", justifyContent:"space-between", alignItems:"center", flexShrink:0 }}>
        <div style={{ fontFamily:"Syne, sans-serif", fontSize:20, fontWeight:800, color:C.accent }}>AdWatch<span style={{color:C.green}}>.</span></div>
        <div style={{ display:"flex", alignItems:"center", gap:10 }}>
          <div style={{ background:C.accentDim, border:`1px solid ${C.accent}33`, borderRadius:100, padding:"5px 14px", fontSize:12, fontWeight:600, color:C.accent }}>{coins} coins</div>
          <Avatar name={user.name} size={32}/>
          <button onClick={onLogout} style={{ background:"transparent", border:"none", cursor:"pointer" }}>
            <Icon n="logout" size={18} color={C.muted}/>
          </button>
        </div>
      </div>

      <div style={{ flex:1, display:"flex", flexDirection:"column", overflow:"hidden" }}>
        {tab==="earn" && <EarnTab watchHistory={watchHistory} balance={balance} watched={watched} onWatch={setWatching}/>}
        {tab==="wallet" && <WalletTab balance={balance} coins={coins} transactions={trans}/>}
        {tab==="referrals" && <ReferralTab user={user}/>}
        {tab==="leaderboard" && <LeaderboardTab user={user} balance={balance}/>}
      </div>

      <div style={{ background:C.surface, borderTop:`1px solid ${C.border}`, display:"flex", flexShrink:0 }}>
        {tabs.map(t=>(
          <button key={t.key} onClick={()=>setTab(t.key)} style={{ flex:1, padding:"12px 0 10px", background:"transparent", border:"none", cursor:"pointer", display:"flex", flexDirection:"column", alignItems:"center", gap:4 }}>
            <Icon n={t.icon} size={20} color={tab===t.key?C.accent:C.muted}/>
            <span style={{ fontSize:10, color:tab===t.key?C.accent:C.muted, fontWeight:tab===t.key?600:400 }}>{t.label}</span>
            {tab===t.key && <div style={{ width:20, height:2, background:C.accent, borderRadius:99 }}/>}
          </button>
        ))}
      </div>
    </div>
  );
};

// ═════════════════════════════════════════════════════════════
// ROOT
// ═════════════════════════════════════════════════════════════
export default function AdWatchApp() {
  const [user, setUser] = useState(null);
  return user ? <MainApp user={user} onLogout={()=>setUser(null)}/> : <AuthScreen onAuth={setUser}/>;
}