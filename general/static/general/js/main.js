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

function getElementFromDjango(element) {
    if (typeof (element) != 'undefined' && element != null) {
        return (JSON.parse(element.textContent));
    } else {
        return false
    }
}

const app = Vue.createApp({
        delimiters: ['[[', ']]'],
        data() {
            return {
                fileModalVisible: false,
                folderModalVisible: false,

                statusModalVisible: false,
                statuses: Array,
                activeStatus: Object,

                postModalVisible: false,
                posts: Array,
                activePost: Object,
            }
        },
        methods: {
            modalAction(modalType, action) {
                if (modalType == "file") {
                    this.fileModalVisible = action
                } else if (modalType == "folder") {
                    this.folderModalVisible = action
                } else if (modalType == "status") {
                    this.statusModalVisible = action
                } else if (modalType == "post") {
                    this.postModalVisible = action
                }
            },
            fetchPosts() {
                axios.get('https://jsonplaceholder.typicode.com/posts', {})
                    .then((response) => {
                        this.posts = response.data;
                        this.activePost = this.posts[0]
                    })
            },
        },
        components: {
            "modal-template": modalTemplate,
            "instance-sheet": instanceSheet,
        },
        mounted() {
            this.fetchPosts();
            this.statuses = getElementFromDjango(document.getElementById('statuses_json'));
            this.activeStatus = getElementFromDjango(document.getElementById('activeStatus_json'))[0];
        },
    }
);

app.mount('#app')