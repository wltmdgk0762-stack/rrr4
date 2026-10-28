import React, { useState, useEffect } from 'react';
import { ShoppingBag, User, LogOut, Shield, Zap, CheckCircle2, Plus, Minus, Ticket, KeyRound, Lock, Search, RefreshCw, AlertCircle } from 'lucide-react';

const PRODUCTS = {
  "PC 시간 충전": [
    { name: "1시간 권", price: 1200 }, { name: "2시간 권", price: 2400 },
    { name: "3시간 권", price: 3500 }, { name: "5시간 권", price: 5500 },
    { name: "10시간 권", price: 10000 }, { name: "15시간 권", price: 14000 },
    { name: "20시간 권", price: 18000 }, { name: "30시간 권", price: 25000 },
    { name: "심야 패키지(6시간)", price: 5000 }, { name: "주말 정액권(12시간)", price: 12000 }
  ],
  "라면 및 분식": [
    { name: "신라면", price: 3500 }, { name: "진라면(매운맛)", price: 3500 },
    { name: "너구리", price: 3800 }, { name: "짜파게티", price: 4000 },
    { name: "불닭볶음면", price: 4500 }, { name: "치즈불닭볶음면", price: 5000 },
    { name: "안성탕면", price: 3500 }, { name: "참깨라면", price: 4000 },
    { name: "떡볶이", price: 4500 }, { name: "치즈떡볶이", price: 5500 },
    { name: "군만두(5개)", price: 3000 }, { name: "김말이(3개)", price: 3000 },
    { name: "소떡소떡", price: 3500 }, { name: "치킨팝콘", price: 4000 }, { name: "감자튀김", price: 4500 }
  ],
  "식사류": [
    { name: "스팸계란간장덮밥", price: 6000 }, { name: "참치마요덮밥", price: 5500 },
    { name: "치킨마요덮밥", price: 6000 }, { name: "제육덮밥", price: 7000 },
    { name: "김치볶음밥", price: 6500 }, { name: "치즈김치볶음밥", price: 7200 },
    { name: "떡만둣국", price: 6500 }, { name: "라면세트", price: 5500 },
    { name: "돈까스덮밥", price: 7500 }, { name: "불고기버거세트", price: 6000 }
  ],
  "스낵 및 과자": [
    { name: "새우깡", price: 2000 }, { name: "포카칩", price: 2000 },
    { name: "양파링", price: 2000 }, { name: "콘칩", price: 2000 },
    { name: "오징어집", price: 2200 }, { name: "홈런볼", price: 2500 },
    { name: "초코파이", price: 1500 }, { name: "칙촉", price: 1800 },
    { name: "프레첼", price: 2000 }, { name: "구운감자", price: 2000 }
  ],
  "음료 및 카페": [
    { name: "콜라(캔)", price: 2000 }, { name: "사이다(캔)", price: 2000 },
    { name: "제로콜라", price: 2200 }, { name: "환타", price: 2000 },
    { name: "몬스터에너지", price: 3000 }, { name: "핫식스", price: 2500 },
    { name: "레쓰비", price: 1500 }, { name: "포카리스웨트", price: 2200 },
    { name: "아이스 아메리카노", price: 3000 }, { name: "복숭아 아이스티", price: 3500 },
    { name: "초코라떼", price: 4000 }, { name: "밀키스", price: 2200 },
    { name: "박카스", price: 1500 }, { name: "생수", price: 1000 }, { name: "망고스무디", price: 4500 }
  ]
};

export default function App() {
  const [view, setView] = useState('MAIN'); // MAIN, REG, LOGIN, FIND_PW, SHOP, SEAT, CASH, RECEIPT, ADMIN
  const [activeCategory, setActiveCategory] = useState("PC 시간 충전");
  
  const [customers, setCustomers] = useState(() => {
    try {
      const saved = localStorage.getItem('pc_customers');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [adminAuth, setAdminAuth] = useState(() => {
    try {
      const saved = localStorage.getItem('pc_admin_auth');
      return saved ? JSON.parse(saved) : { id: 'admin', pw: '1234' };
    } catch {
      return { id: 'admin', pw: '1234' };
    }
  });

  const [currentUser, setCurrentUser] = useState(null);
  const [cart, setCart] = useState([]);
  const [seats, setSeats] = useState(Array.from({ length: 30 }, (_, i) => ({ id: i + 1, taken: i % 7 === 0 })));
  const [selectedSeat, setSelectedSeat] = useState(null);
  
  // Registration Form
  const [regName, setRegName] = useState("");
  const [regPhone, setRegPhone] = useState("");
  const [regPw, setRegPw] = useState("");

  // Login Form
  const [loginPhone, setLoginPhone] = useState("");
  const [loginPw, setLoginPw] = useState("");

  // Find & Reset Password Form
  const [findPhone, setFindPhone] = useState("");
  const [findName, setFindName] = useState("");
  const [foundUser, setFoundUser] = useState(null);
  const [newPassword, setNewPassword] = useState("");

  // User Password Change (Inside Dashboard)
  const [showUserPwModal, setShowUserPwModal] = useState(false);
  const [currUserPw, setCurrUserPw] = useState("");
  const [newUserPw, setNewUserPw] = useState("");

  // Payment Cash State
  const [insertedCash, setInsertedCash] = useState(0);
  const [useCoupon, setUseCoupon] = useState(false);
  const [receiptData, setReceiptData] = useState(null);

  // Admin State
  const [adminId, setAdminId] = useState("");
  const [adminPwInput, setAdminPwInput] = useState("");
  const [isAdminLoggedIn, setIsAdminLoggedIn] = useState(false);
  const [newAdminPw, setNewAdminPw] = useState("");

  useEffect(() => {
    try {
      localStorage.setItem('pc_customers', JSON.stringify(customers));
    } catch (e) {
      console.error(e);
    }
  }, [customers]);

  useEffect(() => {
    try {
      localStorage.setItem('pc_admin_auth', JSON.stringify(adminAuth));
    } catch (e) {
      console.error(e);
    }
  }, [adminAuth]);

  const formatPhone = (val) => {
    const d = val.replace(/\D/g, '');
    if (d.length === 11) return `${d.slice(0, 3)}-${d.slice(3, 7)}-${d.slice(7)}`;
    if (d.length === 10) return `${d.slice(0, 3)}-${d.slice(3, 6)}-${d.slice(6)}`;
    return val;
  };

  const handleRegister = (e) => {
    e.preventDefault();
    if (!regName.trim()) return alert("이름을 입력해주세요.");
    const cleanPhone = regPhone.replace(/\D/g, '');
    if (cleanPhone.length < 10) return alert("올바른 전화번호를 입력하세요.");
    if (!regPw.trim()) return alert("비밀번호를 입력해주세요.");
    
    const formatted = formatPhone(regPhone);
    if (customers.some(c => c.phone === formatted)) return alert("이미 등록된 전화번호입니다.");

    const newUser = {
      name: regName.trim(),
      phone: formatted,
      pw: regPw.trim(),
      points: 0,
      coupons: ["신규가입 500원 할인쿠폰"],
      history: []
    };

    setCustomers([...customers, newUser]);
    setCurrentUser(newUser);
    alert(`🎉 ${newUser.name}님 환영합니다! 신규 500원 할인 쿠폰이 발급되었습니다.`);
    setRegName(""); setRegPhone(""); setRegPw("");
    setView('SHOP');
  };

  const handleLogin = (e) => {
    e.preventDefault();
    const formatted = formatPhone(loginPhone);
    const user = customers.find(c => c.phone === formatted);
    if (!user) return alert("등록되지 않은 전화번호입니다.");
    if (user.pw && user.pw !== loginPw.trim()) return alert("비밀번호가 일치하지 않습니다.");

    setCurrentUser(user);
    setLoginPhone(""); setLoginPw("");
    setView('SHOP');
  };

  const handleFindPassword = (e) => {
    e.preventDefault();
    const formatted = formatPhone(findPhone);
    const user = customers.find(c => c.phone === formatted && c.name === findName.trim());
    if (!user) {
      alert("입력하신 이름과 전화번호가 일치하는 회원을 찾을 수 없습니다.");
      setFoundUser(null);
      return;
    }
    setFoundUser(user);
  };

  const handleResetPassword = (e) => {
    e.preventDefault();
    if (!newPassword.trim()) return alert("새로운 비밀번호를 입력해주세요.");
    
    const updatedCustomers = customers.map(c => c.phone === foundUser.phone ? { ...c, pw: newPassword.trim() } : c);
    setCustomers(updatedCustomers);
    alert("비밀번호가 성공적으로 변경되었습니다! 새 비밀번호로 로그인해주세요.");
    setFoundUser(null);
    setFindName(""); setFindPhone(""); setNewPassword("");
    setView('LOGIN');
  };

  const handleChangeUserPassword = (e) => {
    e.preventDefault();
    if (currentUser.pw && currentUser.pw !== currUserPw.trim()) {
      return alert("현재 비밀번호가 일치하지 않습니다.");
    }
    if (!newUserPw.trim()) return alert("새 비밀번호를 입력해주세요.");

    const updatedUser = { ...currentUser, pw: newUserPw.trim() };
    setCustomers(customers.map(c => c.phone === currentUser.phone ? updatedUser : c));
    setCurrentUser(updatedUser);
    alert("비밀번호가 성공적으로 수정되었습니다.");
    setShowUserPwModal(false);
    setCurrUserPw(""); setNewUserPw("");
  };

  const addToCart = (product) => {
    setCart(prev => {
      const existing = prev.find(item => item.name === product.name);
      if (existing) {
        return prev.map(item => item.name === product.name ? { ...item, qty: item.qty + 1 } : item);
      }
      return [...prev, { ...product, qty: 1 }];
    });
  };

  const updateQty = (name, delta) => {
    setCart(prev => prev.map(item => {
      if (item.name === name) {
        const newQty = item.qty + delta;
        return newQty > 0 ? { ...item, qty: newQty } : null;
      }
      return item;
    }).filter(Boolean));
  };

  const subtotal = cart.reduce((acc, item) => acc + item.price * item.qty, 0);
  const discount = (useCoupon && currentUser?.coupons?.length > 0) ? 500 : 0;
  const finalTotal = Math.max(0, subtotal - discount);

  const addPresetCash = (amount) => {
    setInsertedCash(prev => prev + amount);
  };

  const finishPayment = () => {
    if (insertedCash < finalTotal) {
      alert(`⚠️ 현금이 ${finalTotal - insertedCash}원 부족합니다. 현금을 추가로 투입하세요!`);
      return;
    }

    const change = insertedCash - finalTotal;
    const pointsEarned = Math.floor(finalTotal * 0.05);

    setSeats(prev => prev.map(s => s.id === selectedSeat ? { ...s, taken: true } : s));

    if (currentUser && currentUser.phone !== "010-0000-0000") {
      const updatedCoupons = useCoupon ? currentUser.coupons.slice(1) : currentUser.coupons;
      const updatedUser = {
        ...currentUser,
        points: currentUser.points + pointsEarned,
        coupons: updatedCoupons,
        history: [...currentUser.history, { date: new Date().toLocaleString(), seat: selectedSeat, items: cart, total: finalTotal }]
      };
      setCustomers(customers.map(c => c.phone === currentUser.phone ? updatedUser : c));
      setCurrentUser(updatedUser);
    }

    setReceiptData({
      user: currentUser ? currentUser.name : "비회원",
      phone: currentUser ? currentUser.phone : "-",
      seat: selectedSeat,
      items: cart,
      subtotal,
      discount,
      finalTotal,
      insertedCash,
      change,
      pointsEarned
    });

    setCart([]);
    setInsertedCash(0);
    setUseCoupon(false);
    setView('RECEIPT');
  };

  const handleAdminLogin = (e) => {
    e.preventDefault();
    if (adminId === adminAuth.id && adminPwInput === adminAuth.pw) {
      setIsAdminLoggedIn(true);
      setView('ADMIN');
    } else {
      alert(`관리자 비밀번호가 일치하지 않습니다. (현재 비번: ${adminAuth.pw})`);
    }
  };

  const handleAdminPwChange = (e) => {
    e.preventDefault();
    if (!newAdminPw.trim()) return alert("새 관리자 비밀번호를 입력해주세요.");
    setAdminAuth({ ...adminAuth, pw: newAdminPw.trim() });
    alert("관리자 비밀번호가 успешно 수정되었습니다.");
    setNewAdminPw("");
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-orange-500 selection:text-white">
      {/* Top Header */}
      <header className="bg-slate-900/90 backdrop-blur border-b border-orange-500/20 px-6 py-4 flex justify-between items-center sticky top-0 z-50">
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setView('MAIN')}>
          <div className="bg-gradient-to-tr from-orange-600 to-amber-500 p-2.5 rounded-xl shadow-lg shadow-orange-500/20">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-black tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-amber-200">
              NEXON PC CAFE
            </h1>
            <p className="text-xs text-slate-400 font-mono">KIOSK SYSTEM v3.0</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          {currentUser ? (
            <div className="flex items-center gap-3 bg-slate-800/80 px-4 py-2 rounded-xl border border-slate-700">
              <User className="w-4 h-4 text-orange-400" />
              <span className="text-sm font-bold">{currentUser.name} 회원님</span>
              <span className="text-xs bg-orange-500/20 text-orange-400 px-2 py-0.5 rounded-md font-mono">
                {currentUser.points}P
              </span>
              <button onClick={() => setShowUserPwModal(true)} title="비밀번호 수정" className="text-slate-400 hover:text-orange-400 ml-1">
                <KeyRound className="w-4 h-4" />
              </button>
              <button onClick={() => { setCurrentUser(null); setView('MAIN'); }} title="로그아웃" className="text-slate-400 hover:text-rose-400 ml-1">
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <button onClick={() => setView('ADMIN')} className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-orange-400 bg-slate-800/50 px-3 py-1.5 rounded-lg border border-slate-700">
              <Shield className="w-3.5 h-3.5" />
              관리자
            </button>
          )}
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto flex flex-col justify-center">
        {view === 'MAIN' && (
          <div className="space-y-8 my-auto">
            <div className="text-center space-y-3">
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-orange-500/10 text-orange-400 border border-orange-500/20">
                PREMIUM PC CAFE
              </span>
              <h2 className="text-4xl font-extrabold text-slate-50">원하시는 서비스를 선택하세요</h2>
              <p className="text-slate-400">초고속 PC 이용권 및 맛있고 다양한 먹거리를 편하게 주문하세요.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div onClick={() => setView('LOGIN')} className="group bg-slate-900 border border-slate-800 hover:border-orange-500/50 p-8 rounded-2xl cursor-pointer transition-all duration-300 hover:-translate-y-1 flex flex-col items-center text-center">
                <div className="w-16 h-16 bg-orange-500/10 text-orange-400 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-orange-500 group-hover:text-white transition-colors">
                  <User className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-bold mb-2">회원 로그인</h3>
                <p className="text-sm text-slate-400">전화번호와 비밀번호로 안전하게 로그인하세요.</p>
              </div>

              <div onClick={() => setView('REG')} className="group bg-slate-900 border border-slate-800 hover:border-emerald-500/50 p-8 rounded-2xl cursor-pointer transition-all duration-300 hover:-translate-y-1 flex flex-col items-center text-center">
                <div className="w-16 h-16 bg-emerald-500/10 text-emerald-400 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-emerald-500 group-hover:text-white transition-colors">
                  <Ticket className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-bold mb-2">신규 회원가입</h3>
                <p className="text-sm text-slate-400">신규 가입 즉시 500원 할인 쿠폰이 발급됩니다.</p>
              </div>

              <div onClick={() => { setCurrentUser({ name: "비회원", phone: "010-0000-0000", points: 0, coupons: [] }); setView('SHOP'); }} className="group bg-slate-900 border border-slate-800 hover:border-purple-500/50 p-8 rounded-2xl cursor-pointer transition-all duration-300 hover:-translate-y-1 flex flex-col items-center text-center">
                <div className="w-16 h-16 bg-purple-500/10 text-purple-400 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-purple-500 group-hover:text-white transition-colors">
                  <ShoppingBag className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-bold mb-2">비회원 이용</h3>
                <p className="text-sm text-slate-400">회원 가입 없이 빠르게 시간 충전 및 먹거리를 주문합니다.</p>
              </div>
            </div>
          </div>
        )}

        {view === 'REG' && (
          <div className="max-w-md mx-auto w-full bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-6">
            <h2 className="text-2xl font-bold text-center">신규 회원 가입</h2>
            <form onSubmit={handleRegister} className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-400">이름</label>
                <input type="text" value={regName} onChange={e => setRegName(e.target.value)} placeholder="이름 입력" className="w-full mt-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-orange-500" />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-400">전화번호</label>
                <input type="text" value={regPhone} onChange={e => setRegPhone(e.target.value)} placeholder="010-1234-5678" className="w-full mt-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-orange-500" />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-400">비밀번호</label>
                <input type="password" value={regPw} onChange={e => setRegPw(e.target.value)} placeholder="비밀번호 입력" className="w-full mt-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-orange-500" />
              </div>
              <button type="submit" className="w-full bg-orange-600 hover:bg-orange-500 text-white font-bold py-3.5 rounded-xl transition-colors">가입 및 할인쿠폰 받기</button>
            </form>
            <button onClick={() => setView('MAIN')} className="w-full text-xs text-slate-500 hover:text-slate-300">취소하고 메인으로</button>
          </div>
        )}

        {view === 'LOGIN' && (
          <div className="max-w-md mx-auto w-full bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-6">
            <h2 className="text-2xl font-bold text-center">회원 로그인</h2>
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-400">전화번호 입력</label>
                <input type="text" value={loginPhone} onChange={e => setLoginPhone(e.target.value)} placeholder="01012345678" className="w-full mt-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-orange-500" />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-400">비밀번호 입력</label>
                <input type="password" value={loginPw} onChange={e => setLoginPw(e.target.value)} placeholder="비밀번호" className="w-full mt-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-orange-500" />
              </div>
              <button type="submit" className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3.5 rounded-xl transition-colors">로그인하기</button>
            </form>
            
            <div className="flex justify-between items-center text-xs text-slate-400 pt-2">
              <button onClick={() => setView('FIND_PW')} className="hover:text-orange-400 underline">비밀번호를 잊으셨나요? (비밀번호 찾기)</button>
              <button onClick={() => setView('MAIN')} className="hover:text-slate-300">메인으로</button>
            </div>
          </div>
        )}

        {/* 비밀번호 찾기 및 재설정 뷰 */}
        {view === 'FIND_PW' && (
          <div className="max-w-md mx-auto w-full bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-6">
            <h2 className="text-2xl font-bold text-center flex items-center justify-center gap-2">
              <Search className="w-6 h-6 text-orange-400" />
              비밀번호 찾기
            </h2>

            {!foundUser ? (
              <form onSubmit={handleFindPassword} className="space-y-4">
                <p className="text-xs text-slate-400 text-center">가입 시 입력하신 이름과 전화번호를 입력하세요.</p>
                <div>
                  <label className="text-xs font-semibold text-slate-400">이름</label>
                  <input type="text" value={findName} onChange={e => setFindName(e.target.value)} placeholder="이름 입력" className="w-full mt-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-orange-500" />
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-400">전화번호</label>
                  <input type="text" value={findPhone} onChange={e => setFindPhone(e.target.value)} placeholder="010-1234-5678" className="w-full mt-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-orange-500" />
                </div>
                <button type="submit" className="w-full bg-orange-600 hover:bg-orange-500 text-white font-bold py-3.5 rounded-xl transition-colors">회원 정보 확인</button>
              </form>
            ) : (
              <form onSubmit={handleResetPassword} className="space-y-4">
                <div className="bg-emerald-500/10 border border-emerald-500/30 p-3 rounded-xl text-xs text-emerald-400 text-center">
                  ✅ {foundUser.name} 회원님이 확인되었습니다.<br/>새로운 비밀번호를 입력해주세요.
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-400">새 비밀번호 입력</label>
                  <input type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)} placeholder="새 비밀번호 입력" className="w-full mt-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-orange-500" />
                </div>
                <button type="submit" className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3.5 rounded-xl transition-colors">비밀번호 변경하기</button>
              </form>
            )}

            <button onClick={() => { setFoundUser(null); setView('LOGIN'); }} className="w-full text-xs text-slate-500 hover:text-slate-300">로그인 화면으로 돌아가기</button>
          </div>
        )}

        {view === 'SHOP' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[78vh]">
            <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col h-full overflow-hidden">
              <div className="flex gap-2 border-b border-slate-800 pb-4 overflow-x-auto">
                {Object.keys(PRODUCTS).map(cat => (
                  <button key={cat} onClick={() => setActiveCategory(cat)} className={`px-4 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-colors ${activeCategory === cat ? 'bg-orange-500 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}>
                    {cat}
                  </button>
                ))}
              </div>

              <div className="flex-1 overflow-y-auto mt-4 pr-1 grid grid-cols-2 sm:grid-cols-3 gap-3">
                {PRODUCTS[activeCategory].map((p, idx) => (
                  <div key={idx} onClick={() => addToCart(p)} className="bg-slate-800/60 border border-slate-700/50 hover:border-orange-500 p-4 rounded-xl cursor-pointer transition-all flex flex-col justify-between group">
                    <div>
                      <h4 className="font-bold text-sm text-slate-200 group-hover:text-orange-400">{p.name}</h4>
                      <p className="text-xs text-orange-400 font-mono font-semibold mt-1">{p.price.toLocaleString()}원</p>
                    </div>
                    <button className="mt-3 w-full bg-slate-700 group-hover:bg-orange-600 text-white text-xs font-bold py-1.5 rounded-lg transition-colors flex items-center justify-center gap-1">
                      <Plus className="w-3.5 h-3.5" /> 담기
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col h-full justify-between">
              <div>
                <h3 className="text-lg font-bold border-b border-slate-800 pb-3 flex items-center gap-2">
                  <ShoppingBag className="w-5 h-5 text-orange-400" />
                  장바구니 ({cart.reduce((a, b) => a + b.qty, 0)})
                </h3>
                <div className="max-h-[350px] overflow-y-auto space-y-3 mt-4 pr-1">
                  {cart.length === 0 ? (
                    <p className="text-slate-500 text-center text-xs py-10">담긴 상품이 없습니다.</p>
                  ) : (
                    cart.map(item => (
                      <div key={item.name} className="flex justify-between items-center bg-slate-800/50 p-3 rounded-xl">
                        <div>
                          <p className="text-xs font-bold">{item.name}</p>
                          <p className="text-xs text-slate-400 font-mono">{(item.price * item.qty).toLocaleString()}원</p>
                        </div>
                        <div className="flex items-center gap-2">
                          <button onClick={() => updateQty(item.name, -1)} className="p-1 bg-slate-700 rounded text-slate-300 hover:bg-slate-600"><Minus className="w-3 h-3" /></button>
                          <span className="text-xs font-mono font-bold w-4 text-center">{item.qty}</span>
                          <button onClick={() => updateQty(item.name, 1)} className="p-1 bg-slate-700 rounded text-slate-300 hover:bg-slate-600"><Plus className="w-3 h-3" /></button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              <div className="border-t border-slate-800 pt-4 space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">총 금액</span>
                  <span className="font-bold text-orange-400 font-mono text-lg">{subtotal.toLocaleString()}원</span>
                </div>
                <button disabled={cart.length === 0} onClick={() => setView('SEAT')} className="w-full bg-orange-600 hover:bg-orange-500 disabled:bg-slate-800 disabled:text-slate-600 text-white font-bold py-3.5 rounded-xl transition-colors">
                  좌석 선택하기 →
                </button>
              </div>
            </div>
          </div>
        )}

        {view === 'SEAT' && (
          <div className="max-w-4xl mx-auto w-full bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-6">
            <h2 className="text-2xl font-bold text-center">PC방 좌석 선택 (1~30번)</h2>
            <div className="grid grid-cols-6 gap-3">
              {seats.map(s => (
                <button key={s.id} disabled={s.taken} onClick={() => setSelectedSeat(s.id)} className={`p-4 rounded-xl border font-bold text-center transition-all ${s.taken ? 'bg-rose-950/40 border-rose-800/50 text-rose-500 cursor-not-allowed' : selectedSeat === s.id ? 'bg-orange-500 border-orange-400 text-white ring-2 ring-orange-500/50' : 'bg-slate-800 border-slate-700 hover:border-slate-500 text-slate-200'}`}>
                  {s.id}번
                  <span className="block text-[10px] mt-1 font-normal opacity-80">{s.taken ? "사용중" : "공석"}</span>
                </button>
              ))}
            </div>
            <div className="flex gap-4">
              <button onClick={() => setView('SHOP')} className="w-1/3 bg-slate-800 hover:bg-slate-700 py-3 rounded-xl font-bold">뒤로가기</button>
              <button disabled={!selectedSeat} onClick={() => setView('CASH')} className="w-2/3 bg-orange-600 hover:bg-orange-500 disabled:bg-slate-800 disabled:text-slate-600 py-3 rounded-xl font-bold">
                결제 진행하기 (선택: {selectedSeat}번) →
              </button>
            </div>
          </div>
        )}

        {view === 'CASH' && (
          <div className="max-w-md mx-auto w-full bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-6">
            <div className="text-center space-y-1">
              <h2 className="text-xl font-bold">현금 지불 투입기</h2>
              <p className="text-xs text-slate-400">결제할 현금을 직접 투입해주세요.</p>
            </div>

            {currentUser?.coupons?.length > 0 && (
              <div className="bg-orange-500/10 border border-orange-500/30 p-3 rounded-xl flex items-center justify-between">
                <span className="text-xs text-orange-300 font-semibold">500원 할인 쿠폰 보유 중</span>
                <button onClick={() => setUseCoupon(!useCoupon)} className={`text-xs px-3 py-1 rounded-lg font-bold ${useCoupon ? 'bg-orange-500 text-white' : 'bg-slate-800 text-slate-300'}`}>
                  {useCoupon ? "적용됨 (-500원)" : "사용하기"}
                </button>
              </div>
            )}

            <div className="bg-slate-950 p-4 rounded-xl space-y-2 border border-slate-800 font-mono text-sm">
              <div className="flex justify-between text-slate-400"><span>총 주문금액</span><span>{subtotal.toLocaleString()}원</span></div>
              {useCoupon && <div className="flex justify-between text-emerald-400"><span>쿠폰 할인</span><span>-500원</span></div>}
              <div className="flex justify-between text-slate-200 font-bold border-t border-slate-800 pt-2 text-base"><span>최종 결제액</span><span className="text-orange-400">{finalTotal.toLocaleString()}원</span></div>
              <div className="flex justify-between text-amber-400 font-bold border-t border-slate-800 pt-2"><span>투입된 현금</span><span>{insertedCash.toLocaleString()}원</span></div>
            </div>

            <div className="grid grid-cols-2 gap-2">
              {[1000, 5000, 10000, 50000].map(amt => (
                <button key={amt} onClick={() => addPresetCash(amt)} className="bg-slate-800 hover:bg-slate-700 py-2.5 rounded-xl font-mono font-bold text-xs text-slate-200">
                  +{amt.toLocaleString()}원 투입
                </button>
              ))}
            </div>

            <button onClick={finishPayment} className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3.5 rounded-xl transition-colors">
              결제 완료하기
            </button>
          </div>
        )}

        {view === 'RECEIPT' && receiptData && (
          <div className="max-w-md mx-auto w-full bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-6">
            <div className="text-center space-y-1">
              <CheckCircle2 className="w-12 h-12 text-emerald-400 mx-auto" />
              <h2 className="text-2xl font-bold">결제 및 영수증 완료</h2>
            </div>

            <div className="bg-white text-slate-900 p-6 rounded-xl font-mono text-xs space-y-3 shadow-inner">
              <div className="text-center border-b border-dashed border-slate-300 pb-3">
                <p className="font-bold text-sm">NEXON PC CAFE</p>
                <p className="text-[10px] text-slate-500">영수증 및 주문 확인서</p>
              </div>
              <p>고객명: {receiptData.user} ({receiptData.phone})</p>
              <p>배정좌석: {receiptData.seat}번 PC</p>
              <div className="border-t border-b border-slate-200 py-2 space-y-1">
                {receiptData.items.map(item => (
                  <div key={item.name} className="flex justify-between">
                    <span>{item.name} x{item.qty}</span>
                    <span>{(item.price * item.qty).toLocaleString()}원</span>
                  </div>
                ))}
              </div>
              <div className="space-y-1 pt-1 font-bold">
                <div className="flex justify-between"><span>결제금액</span><span>{receiptData.finalTotal.toLocaleString()}원</span></div>
                <div className="flex justify-between"><span>투입금액</span><span>{receiptData.insertedCash.toLocaleString()}원</span></div>
                <div className="flex justify-between text-orange-600"><span>거스름돈</span><span>{receiptData.change.toLocaleString()}원</span></div>
                <div className="flex justify-between text-emerald-600"><span>적립포인트</span><span>+{receiptData.pointsEarned}P</span></div>
              </div>
            </div>

            <button onClick={() => setView('MAIN')} className="w-full bg-orange-600 hover:bg-orange-500 text-white font-bold py-3.5 rounded-xl transition-colors">
              처음 화면으로 돌아가기
            </button>
          </div>
        )}

        {view === 'ADMIN' && (
          <div className="max-w-2xl mx-auto w-full bg-slate-900 border border-slate-800 p-8 rounded-2xl space-y-6">
            <h2 className="text-2xl font-bold text-center">관리자 시스템</h2>
            {!isAdminLoggedIn ? (
              <form onSubmit={handleAdminLogin} className="space-y-4 max-w-sm mx-auto">
                <input type="text" value={adminId} onChange={e => setAdminId(e.target.value)} placeholder="관리자 ID (admin)" className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white" />
                <input type="password" value={adminPwInput} onChange={e => setAdminPwInput(e.target.value)} placeholder="관리자 비밀번호" className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white" />
                <button type="submit" className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl">로그인</button>
              </form>
            ) : (
              <div className="space-y-6">
                <div className="space-y-3">
                  <h3 className="font-bold text-slate-300">등록 회원 목록 ({customers.length}명)</h3>
                  <div className="bg-slate-950 p-4 rounded-xl max-h-48 overflow-y-auto space-y-2 text-xs">
                    {customers.map((c, i) => (
                      <div key={i} className="flex justify-between border-b border-slate-800 pb-2">
                        <span>{c.name} ({c.phone})</span>
                        <span className="text-orange-400 font-mono">{c.points}P | 쿠폰 {c.coupons.length}장</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* 관리자 비밀번호 변경 섹션 */}
                <form onSubmit={handleAdminPwChange} className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
                  <h4 className="text-sm font-bold text-orange-400">🔑 관리자 비밀번호 변경</h4>
                  <div className="flex gap-2">
                    <input type="password" value={newAdminPw} onChange={e => setNewAdminPw(e.target.value)} placeholder="새 관리자 비밀번호" className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white" />
                    <button type="submit" className="bg-orange-600 hover:bg-orange-500 px-4 py-2 rounded-xl text-xs font-bold">변경</button>
                  </div>
                </form>

                <button onClick={() => setSeats(Array.from({ length: 30 }, (_, i) => ({ id: i + 1, taken: false })))} className="w-full bg-rose-600 hover:bg-rose-500 py-3 rounded-xl font-bold text-xs">
                  모든 좌석 공석 초기화
                </button>
                <button onClick={() => setView('MAIN')} className="w-full bg-slate-800 py-3 rounded-xl font-bold text-xs">메인으로 돌아가기</button>
              </div>
            )}
          </div>
        )}
      </main>

      {/* 사용자 비밀번호 변경 모달 */}
      {showUserPwModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl max-w-sm w-full space-y-4">
            <h3 className="text-lg font-bold">🔒 비밀번호 수정</h3>
            <form onSubmit={handleChangeUserPassword} className="space-y-3">
              <div>
                <label className="text-xs text-slate-400">현재 비밀번호</label>
                <input type="password" value={currUserPw} onChange={e => setCurrUserPw(e.target.value)} placeholder="현재 비밀번호 입력" className="w-full mt-1 bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white" />
              </div>
              <div>
                <label className="text-xs text-slate-400">새 비밀번호</label>
                <input type="password" value={newUserPw} onChange={e => setNewUserPw(e.target.value)} placeholder="새 비밀번호 입력" className="w-full mt-1 bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white" />
              </div>
              <div className="flex gap-2 pt-2">
                <button type="button" onClick={() => setShowUserPwModal(false)} className="w-1/2 bg-slate-800 py-2.5 rounded-xl text-xs font-bold">취소</button>
                <button type="submit" className="w-1/2 bg-orange-600 hover:bg-orange-500 py-2.5 rounded-xl text-xs font-bold">수정하기</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
