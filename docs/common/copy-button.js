function createCopyButton(targetId, buttonText = '⧉ Copy') {
    const target = document.getElementById(targetId);
    if (!target) {
        console.error('Target element not found:', targetId);
        return;
    }
    
    // コンテナを作成
    const container = document.createElement('div');
    container.className = 'copy-container';
    
    // 親要素から対象を取り出してコンテナに移動
    const parent = target.parentNode;
    parent.insertBefore(container, target);
    container.appendChild(target);
    
    // コピーボタンを作成
    const button = document.createElement('button');
    button.className = 'copy-button';
    button.textContent = buttonText;
    button.onclick = () => copyToClipboard(target, button);
    
    container.appendChild(button);
}

function copyToClipboard(element, button) {
    const text = element.innerText || element.textContent;
    
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            showCopySuccess(button);
        }).catch(err => {
            alert('コピーに失敗しました: ' + err);
        });
    } else {
        // フォールバック: 古いブラウザ対応
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            showCopySuccess(button);
        } catch (err) {
            alert('コピーに失敗しました');
        }
        document.body.removeChild(textarea);
    }
}

function showCopySuccess(button) {
    const originalText = button.textContent;
    button.textContent = '✓ コピー完了!';
    button.classList.add('success');
    setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove('success');
    }, 2000);
}