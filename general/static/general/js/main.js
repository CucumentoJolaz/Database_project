function confirmDeletion(e) {
    var txt;
    if (!confirm("Вы уверены в удалении?")) {
        e.preventDefault();
    }
    document.getElementById("demo").innerHTML = txt;
}

function confirmApproval(e) {
    var txt;
    if (!confirm("Вы уверены в утверждении?")) {
        e.preventDefault();
    }
    document.getElementById("demo").innerHTML = txt;
}

const app = Vue.createApp({
        delimiters: ['[[', ']]'],
        data() {
            return {
                fileModalVisible: false,
                folderModalVisible: false,
            }
        },
        methods: {
            showFileModal() {
                this.fileModalVisible = true
            },
            showFolderModal() {
                this.folderModalVisible = true
            },
        },
        components: {
            "modal-template": modalTemplate,
        }

    }
);

app.mount('#app')