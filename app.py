import streamlit as st
import streamlit.components.v1 as components
import json

def main():
    st.set_page_config(layout="wide", page_title="Accumulated Data Keyboard")

    # --- CSS設定 ---
    st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                padding-left: 0.5rem;
                padding-right: 0.5rem;
                max-width: 100%;
            }
            iframe {
                width: 100% !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("大きさの変わるキーボードアプリ")
    st.caption("「送信（Next Trial）」を押すことで、データを保持したまま次の入力へ進めます。")

    # サイドバー設定
    with st.sidebar:

        st.header("拡大機能の設定")
        scale_enabled = st.checkbox("拡大機能 ON/OFF", value=True)
        st.divider()
    
        st.header("キーボードサイズの設定")
        breath_speed = st.slider("変化速度 (秒)", 0.1, 5.0, 2.0, 0.1)
        scale_min = st.slider("最小サイズ", 0.5, 1.0, 0.8, 0.01)
        scale_max = st.slider("最大サイズ", 1.0, 1.5, 1.1, 0.01)

        st.divider()

        st.header("移動機能の設定")
        move_enabled = st.sidebar.checkbox("移動機能 ON/OFF", value=True)

        st.divider()

        st.header("キーボード移動の設定")
        move_speed = st.slider("移動速度(秒)", 1.0, 20.0, 5.0, 0.5)
        move_range = st.slider("移動範囲(px)", 0, 200, 30, 5)

        st.divider()
        st.header("移動規則性の設定")

    # --- キーボードデータ ---
    rows = [
        # Row 1
        [
            {"label": "~", "sub": "`", "val": "`", "w": 1},
            {"label": "!", "sub": "1 ぬ", "val": "1", "w": 1},
            {"label": "@", "sub": "2 ふ", "val": "2", "w": 1},
            {"label": "#", "sub": "3 あ", "val": "3", "w": 1},
            {"label": "$", "sub": "4 う", "val": "4", "w": 1},
            {"label": "%", "sub": "5 え", "val": "5", "w": 1},
            {"label": "^", "sub": "6 お", "val": "6", "w": 1},
            {"label": "&", "sub": "7 や", "val": "7", "w": 1},
            {"label": "*", "sub": "8 ゆ", "val": "8", "w": 1},
            {"label": "(", "sub": "9 よ", "val": "9", "w": 1},
            {"label": ")", "sub": "0 わ", "val": "0", "w": 1},
            {"label": "-", "sub": "ー", "val": "-", "w": 1, "color": "yellow"},
            {"label": "+", "sub": "=", "val": "=", "w": 1},
            {"label": "BS", "sub": "", "val": "BS", "w": 2, "align": "right"},
        ],
        # Row 2
        [
            {"label": "Tab", "sub": "", "val": "\t", "w": 1.5, "align": "left"},
            {"label": "Q", "sub": "た", "val": "q", "w": 1},
            {"label": "W", "sub": "て", "val": "w", "w": 1},
            {"label": "E", "sub": "い", "val": "e", "w": 1},
            {"label": "R", "sub": "す", "val": "r", "w": 1, "color": "red"},
            {"label": "T", "sub": "か", "val": "t", "w": 1},
            {"label": "Y", "sub": "ん", "val": "y", "w": 1},
            {"label": "U", "sub": "な", "val": "u", "w": 1},
            {"label": "I", "sub": "に", "val": "i", "w": 1},
            {"label": "O", "sub": "ら", "val": "o", "w": 1},
            {"label": "P", "sub": "せ", "val": "p", "w": 1},
            {"label": "{", "sub": "「", "val": "{", "w": 1, "color": "yellow"},
            {"label": "}", "sub": "」", "val": "}", "w": 1, "color": "yellow"},
            {"label": "|", "sub": "ー", "val": "|", "w": 1, "color": "yellow"},
        ],
        # Row 3
        [
            {"label": "Caps", "sub": "", "val": "", "w": 1.8, "align": "left"},
            {"label": "A", "sub": "ち", "val": "a", "w": 1},
            {"label": "S", "sub": "と", "val": "s", "w": 1},
            {"label": "D", "sub": "し", "val": "d", "w": 1, "color": "red"},
            {"label": "F", "sub": "は", "val": "f", "w": 1, "color": "red"},
            {"label": "G", "sub": "き", "val": "g", "w": 1},
            {"label": "H", "sub": "く", "val": "h", "w": 1},
            {"label": "J", "sub": "ま", "val": "j", "w": 1},
            {"label": "K", "sub": "の", "val": "k", "w": 1},
            {"label": "L", "sub": "り", "val": "l", "w": 1},
            {"label": ":", "sub": ";", "val": ":", "w": 1, "color": "green"},
            {"label": "\"", "sub": "'", "val": "\"", "w": 1, "color": "green"},
            {"label": "Enter", "sub": "", "val": "\n", "w": 2.2, "align": "right"},
        ],
        # Row 4
        [
            {"label": "Shift", "sub": "", "val": "", "w": 2.3, "align": "left"},
            {"label": "Z", "sub": "つ", "val": "z", "w": 1},
            {"label": "X", "sub": "さ", "val": "x", "w": 1, "color": "red"},
            {"label": "C", "sub": "そ", "val": "c", "w": 1, "color": "red"},
            {"label": "V", "sub": "ひ", "val": "v", "w": 1, "color": "red"},
            {"label": "B", "sub": "こ", "val": "b", "w": 1},
            {"label": "N", "sub": "み", "val": "n", "w": 1},
            {"label": "M", "sub": "も", "val": "m", "w": 1},
            {"label": "<", "sub": "、", "val": "<", "w": 1},
            {"label": ">", "sub": "。", "val": ">", "w": 1},
            {"label": "?", "sub": "・", "val": "?", "w": 1},
            {"label": "Shift", "sub": "", "val": "", "w": 2.7, "align": "right"},
        ],
        # Row 5
        [
            {"label": "Ctrl", "sub": "", "val": "", "w": 1.5},
            {"label": "Fn", "sub": "", "val": "", "w": 1},
            {"label": "Win", "sub": "", "val": "", "w": 1},
            {"label": "Alt", "sub": "", "val": "", "w": 1},
            {"label": "", "sub": "", "val": " ", "w": 6},
            {"label": "Alt", "sub": "", "val": "", "w": 1},
            {"label": "Win", "sub": "", "val": "", "w": 1},
            {"label": "Ctrl", "sub": "", "val": "", "w": 1},
            {"label": "←", "sub": "", "val": "", "w": 1},
            {"label": "↑↓", "sub": "", "val": "", "w": 1, "is_arrow": True},
            {"label": "→", "sub": "", "val": "", "w": 1},
        ]
    ]

    rows_json = json.dumps(rows)

    # --- HTML/CSS/JS テンプレート ---
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@500&family=Noto+Sans+JP:wght@400&display=swap');

        body {{
            font-family: 'Roboto Mono', 'Noto Sans JP', monospace;
            background-color: transparent;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            overflow: hidden;
            user-select: none;
        }}

        #screen {{
            width: 95%;
            height: 50px;
            background-color: #333;
            color: #0f0;
            font-size: 20px;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
            border: 2px solid #555;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            font-family: monospace;
            resize: none;
            box-sizing: border-box;
            z-index: 200;
            position: relative;
        }}

        /* コントロールエリア */
        .controls {{
            display: flex;
            gap: 15px;
            margin-top: 10px;
            z-index: 300;
            position: relative;
            align-items: center;
        }}

        button {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-family: 'Noto Sans JP', sans-serif;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            transition: 0.2s;
        }}
        button:active {{ transform: translateY(2px); box-shadow: 0 2px 2px rgba(0,0,0,0.2); }}

        #next-btn {{ background-color: #2196F3; color: white; }}
        #next-btn:hover {{ background-color: #1e88e5; }}

        #download-btn {{ background-color: #4CAF50; color: white; }}
        #download-btn:hover {{ background-color: #45a049; }}

        #reset-btn {{ background-color: #f44336; color: white; font-size: 12px; padding: 8px 12px; }}
        #reset-btn:hover {{ background-color: #d32f2f; }}

        #data-count {{ color: #555; font-size: 14px; font-weight: bold; }}

        /* --- アニメーション --- */
        @keyframes breathe {{
            0% {{ transform: scaleX({scale_min}) scaleY({scale_min}); }}
            50% {{ transform: scaleX({scale_max}) scaleY({scale_max}); }}
            100% {{ transform: scaleX({scale_min}) scaleY({scale_min}); }}
        }}

        @keyframes float {{
            0% {{ transform: translate(0px, 0px); }}
            20% {{ transform: translate({move_range}px, -{move_range/2}px); }}
            40% {{ transform: translate(-{move_range/2}px, {move_range}px); }}
            60% {{ transform: translate(-{move_range}px, -{move_range/2}px); }}
            80% {{ transform: translate({move_range/2}px, {move_range/2}px); }}
            100% {{ transform: translate(0px, 0px); }}
        }}

        .movement-wrapper {{
            animation: float {move_speed}s infinite ease-in-out;
            width: 95%;
            display: flex;
            justify-content: center;
            padding: {move_range}px; 
        }}

        .keyboard-wrapper {{
            animation: breathe {breath_speed}s infinite ease-in-out;
            padding: 10px;
            background-color: #e8eaed;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 100%;
            height: 55vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
        }}

        .kb-row {{
            display: flex;
            justify-content: space-between;
            width: 100%;
            height: 18%;
        }}

        .key {{
            background-color: white;
            border: 1px solid #999;
            border-bottom: 3px solid #777;
            border-radius: 4px;
            margin: 0 1px;
            position: relative;
            cursor: pointer;
            transition: background-color 0.1s;
            user-select: none;
            box-shadow: 0 2px 2px rgba(0,0,0,0.1);
            flex-basis: 0; 
            height: 100%;
            touch-action: none;
        }}

        .key.active {{
            transform: translateY(2px);
            border-bottom: 1px solid #777;
            background-color: #f0f0f0;
        }}

        .label-top {{
            position: absolute; top: 4px; left: 6px; font-size: 14px; color: #333; font-weight: bold;
        }}
        .label-sub {{
            position: absolute; bottom: 4px; right: 6px; font-size: 10px; color: #888;
        }}
        @media (max-width: 800px) {{
             .label-top {{ font-size: 10px; }}
             .label-sub {{ font-size: 8px; }}
        }}
        .color-red {{ background-color: #ea9999; border-color: #c06666; }}
        .color-yellow {{ background-color: #ffe599; border-color: #d1b866; }}
        .color-green {{ background-color: #b6d7a8; border-color: #7b9e6d; }}

        .arrow-stack {{
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100%; font-sizest.divider(): 10px; line-height: 10px;
        }}

    </style>
    </head>
    <body>
        <textarea id="screen" placeholder="ここに入力してください"></textarea>
        
        <div class="movement-wrapper" id="move-wrap">
            <div class="keyboard-wrapper" id="kb-wrap"></div>
        </div>

        <div class="controls">
            <button id="next-btn" onclick="nextTrial()">送信</button>
            <button id="download-btn" onclick="downloadCSV()">CSVをダウンロード</button>
            <span id="data-count">試行回数: 1</span>
            <button id="reset-btn" onclick="resetData()">リセット</button>
        </div>

        <script>
            const rows = {rows_json};
            const kbContainer = document.getElementById('kb-wrap');
            const screen = document.getElementById('screen');
            const dataCountLabel = document.getElementById('data-count');

            // --- セッションストレージからデータを復元（リロード対策） ---
            let recordedData = JSON.parse(sessionStorage.getItem('kb_data') || '[]');
            let currentTrial = parseInt(sessionStorage.getItem('kb_trial') || '1');
            let lastDownTime = null;
            let lastUpTime = null;

            // 初期表示更新
            updateStatus();

            // --- キーボード生成 ---
            rows.forEach(row => {{
                const rowDiv = document.createElement('div');
                rowDiv.className = 'kb-row';

                row.forEach(k => {{
                    const keyDiv = document.createElement('div');
                    keyDiv.className = 'key';
                    keyDiv.style.flexGrow = k.w;
                    
                    if(k.color) keyDiv.classList.add('color-' + k.color);

                    let contentHtml = '';
                    if(k.is_arrow) {{
                        contentHtml = `<div class="arrow-stack"><span>▲</span><span>▼</span></div>`;
                    }} else {{
                        contentHtml = `<span class="label-top">${{k.label || ''}}</span><span class="label-sub">${{k.sub || ''}}</span>`;
                    }}
                    keyDiv.innerHTML = contentHtml;

                    keyDiv.onpointerdown = (e) => {{
                        e.preventDefault();
                        keyDiv.classList.add('active');

                        const now = Date.now();
                        const rect = kbContainer.getBoundingClientRect();
                        const style = window.getComputedStyle(kbContainer);
                        const matrix = new DOMMatrix(style.transform);
                        const currentScale = matrix.a;

                        let downDownTime = lastDownTime ? (now - lastDownTime) : '';
                        let upDownTime = lastUpTime ? (now - lastUpTime) : '';

                        keyDiv._currentData = {{
                            trial: currentTrial, // 試行回数を記録
                            key: k.val || k.label || 'Unknown',
                            downTime: now,
                            downDown: downDownTime,
                            upDown: upDownTime,
                            kbScale: currentScale.toFixed(3),
                            kbX: rect.x.toFixed(1),
                            kbY: rect.y.toFixed(1),
                            pressure: e.pressure || 0,
                            area: (e.width * e.height).toFixed(2)
                        }};

                        lastDownTime = now;
                        
                        if (k.val === 'BS') {{
                            screen.value = screen.value.slice(0, -1);
                        }} else if (k.val) {{
                            screen.value += k.val;
                        }}
                        screen.scrollTop = screen.scrollHeight;
                    }};

                    keyDiv.onpointerup = (e) => {{
                        e.preventDefault();
                        keyDiv.classList.remove('active');
                        
                        if (keyDiv._currentData) {{
                            const now = Date.now();
                            const holdTime = now - keyDiv._currentData.downTime;
                            
                            const record = {{
                                ...keyDiv._currentData,
                                upTime: now,
                                holdTime: holdTime
                            }};
                            
                            recordedData.push(record);
                            
                            // データを保存（永続化）
                            sessionStorage.setItem('kb_data', JSON.stringify(recordedData));
                            
                            lastUpTime = now;
                            updateStatus();
                            keyDiv._currentData = null;
                        }}
                    }};
                    
                    keyDiv.onpointerleave = (e) => {{
                        if (keyDiv.classList.contains('active')) {{
                            keyDiv.dispatchEvent(new PointerEvent('pointerup'));
                        }}
                    }};

                    rowDiv.appendChild(keyDiv);
                }});

                kbContainer.appendChild(rowDiv);
            }});

            // --- ステータス表示更新 ---
            function updateStatus() {{
                dataCountLabel.innerText = `Trial: ${{currentTrial}} | Records: ${{recordedData.length}}`;
            }}

            // --- 次の試行へ（送信） ---
            function nextTrial() {{
                currentTrial++;
                sessionStorage.setItem('kb_trial', currentTrial);
                screen.value = ""; // 入力欄クリア
                updateStatus();
            }}

            // --- データリセット ---
            function resetData() {{
                if(confirm("蓄積された全てのデータを消去しますか？")) {{
                    recordedData = [];
                    currentTrial = 1;
                    sessionStorage.clear();
                    screen.value = "";
                    updateStatus();
                }}
            }}

            // --- CSVダウンロード ---
            function downloadCSV() {{
                if (recordedData.length === 0) {{
                    alert("No data collected yet!");
                    return;
                }}

                const headers = [
                    "Trial", "Key", 
                    "DownTime(ms)", "UpTime(ms)", 
                    "HoldTime(ms)", "DownDown(ms)", "UpDown(ms)",
                    "Scale", "Kb_X", "Kb_Y", 
                    "Pressure", "FingerArea"
                ];

                const csvRows = [headers.join(",")];
                
                recordedData.forEach(d => {{
                    const row = [
                        d.trial, // 試行回数
                        `"${{d.key}}"`,
                        d.downTime,
                        d.upTime,
                        d.holdTime,
                        d.downDown,
                        d.upDown,
                        d.kbScale,
                        d.kbX,
                        d.kbY,
                        d.pressure,
                        d.area
                    ];
                    csvRows.push(row.join(","));
                }});

                const csvString = csvRows.join("\\n");
                const blob = new Blob([csvString], {{ type: "text/csv" }});
                const url = URL.createObjectURL(blob);
                
                const a = document.createElement('a');
                a.href = url;
                a.download = "keyboard_data_accumulated.csv";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }}
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=750, scrolling=False)

if __name__ == "__main__":
    main()
