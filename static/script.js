const dropzone = document.getElementById('dropzone');

dropzone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropzone.classList.add('highlight');
});

dropzone.addEventListener('dragleave', (event) => {
    event.preventDefault();
    dropzone.classList.remove('highlight');
});

// ドロップ時の処理
dropzone.addEventListener('drop', async (event) => {
    event.preventDefault();
    dropzone.classList.remove('highlight'); // ハイライト表示を解除

    const files = event.dataTransfer.files; // ドロップされたファイルを取得

    // ファイルをサーバーに送信する処理を実行
    await sendFilesToServer(files);
    // 画面遷移を実行
});

// ファイルをサーバーに送信する関数
async function sendFilesToServer(files) {
    const formData = new FormData();
    for (const file of files) {
        formData.append('file', file); // ファイルをフォームデータに追加
    }

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            console.log('File(s) uploaded successfully!');
            window.location.href = '/upload'; // ここで'/upload'に遷移

        } else {
            console.error('Error uploading file(s).');
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

// const files = event.dataTransfer.files; // ドロップされたファイルを取得
// // ファイルをサーバーに送信する処理を実行
// await sendFilesToServer(files);

// const file = event.dataTransfer.files[0];
// if (file.type === 'text/csv') {

//     const formData = new FormData();
//     formData.append('file', file);

//     fetch('/upload', {
//         method: 'POST',
//         body: formData
//     });
//     // .then(response => response.json())
//     // .then(data => {
//     //     // Process and display the uploaded CSV data (data variable)
//     //     console.log(data);
//     // });
// } else {
//     alert('Please select a CSV file.');
// }
// });
