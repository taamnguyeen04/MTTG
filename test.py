import streamlit as st
from streamlit.components.v1 import html

keyboard_js = """
<script>
document.addEventListener('keydown', function(e) {
    const output = document.getElementById('key-output');
    if (output) {
        output.innerHTML = `
            <div style="
                padding: 0.5rem;
                background: #ffebee;
                border-radius: 0.5rem;
                margin: 0.5rem 0;
            ">
                <strong>Phím nhấn:</strong> ${e.key}<br>
                <strong>Mã phím:</strong> ${e.code}<br>
                <strong>Tổ hợp phím:</strong> 
                ${e.ctrlKey ? 'Ctrl+' : ''}
                ${e.shiftKey ? 'Shift+' : ''}
                ${e.altKey ? 'Alt+' : ''}
                ${e.metaKey ? 'Meta+' : ''}
            </div>
        `;
    }
});
</script>
"""

st.title("Nhận diện phím bàn phím")
st.write("Nhấn bất kỳ phím nào trên bàn phím...")
html('<div id="key-output" style="min-height: 100px;"></div>')
html(keyboard_js)