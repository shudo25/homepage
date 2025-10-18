// 折り返し切り替え機能
(function() {
    // ページ読み込み時に実行
    document.addEventListener('DOMContentLoaded', function() {
        // PCかどうかを判定（スマホ/タブレット以外ならPCとみなす）
        var isPC = !/iphone|ipad|android|mobile|windows phone|ipod/i.test(navigator.userAgent);
        if (isPC) {
            // PCではボタンを表示せず、常に横スクロール（wrap解除）
            applyWrapMode(false);
            return;
        }
        // --- ここから従来のスマホ/タブレット向け処理 ---
        const savedWrapMode = localStorage.getItem('preWrapMode');
        const wrapMode = savedWrapMode === 'true';
        // ボタンを作成
        const button = document.createElement('button');
        button.className = 'wrap-toggle-button';
        button.textContent = wrapMode ? '横スクロール表示' : '折り返し表示';
        button.setAttribute('aria-label', '行の折り返し表示を切り替え');
        // 初期状態を適用
        if (wrapMode) {
            applyWrapMode(true);
        }
        // ボタンクリック時の処理
        button.addEventListener('click', function() {
            const currentlyWrapping = document.body.classList.contains('wrap-mode-active');
            const newWrapMode = !currentlyWrapping;
            applyWrapMode(newWrapMode);
            button.textContent = newWrapMode ? '横スクロール表示' : '折り返し表示';
            // 設定を保存
            localStorage.setItem('preWrapMode', newWrapMode);
        });
        // ボタンを追加
        document.body.appendChild(button);
    });
    
    // 折り返しモードを適用する関数
    function applyWrapMode(enable) {
        const preElements = document.querySelectorAll('pre');
        
        if (enable) {
            document.body.classList.add('wrap-mode-active');
            preElements.forEach(function(pre) {
                pre.classList.add('wrap-mode');
            });
        } else {
            document.body.classList.remove('wrap-mode-active');
            preElements.forEach(function(pre) {
                pre.classList.remove('wrap-mode');
            });
        }
    }
})();
