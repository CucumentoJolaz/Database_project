const modalTemplate = {
    name: "modal-template",
    template: `
        <div class="dialog"
             v-if="show"
             @click="hideModalWindow">
            <div @click.stop class="dialog__content">
                <header class="dialogHeader">
                    <button
                        type="button"
                        class="btnClose"
                        @click="hideModalWindow">
                        X
                    </button>
                    <slot name="header"
                        @update:show="show">
                    </slot>
                </header>
                <body class="dialogBody">
                     <slot name="body"
                        @update:show="show">
                     </slot>
                </body>
                <footer class="dialogFooter">
                    <slot name="footer"
                        @update:show="show">
                    </slot>
                </footer>
            </div>
        </div>`,
    props: {
        show: {
            type: Boolean,
            default: false
        }
    },
    methods: {
        hideModalWindow() {
            this.$emit('update:show', false)
        }
    },
};

const instanceItem = {
    name: "instance-item",
    template: `
    <div :class="isActive ? 'activeInstanceItem' : 'instanceItem'"
         @click="updateActiveInstance"> 
            <tr>
                <td>{{instance.title}}</td>
            </tr>
    </div>`,
    props: {
        instance: {
            type: Object,
            required: true,
        },
        active_instance: {
            type: Object,
            required: true,
        }
    },
    computed: {
        isActive() {
            if (this.instance.id == this.active_instance.id) {
                return true
            } else return false
        }
    },
    methods: {
        updateActiveInstance() {
            this.$parent.$parent.activeInstance = this.instance
        }
    },

};

const instanceList = {
    name: "instance-list",
    template: `
    <div v-if="instances.length > 0"
         class="instanceList">
        <table class="tableItem">
            <instance-item
            v-for="instance in instances"
            :instance="instance"
            :key="instance.id"
             v-model:active_instance="active_instance"
            />
        </table>   
    </div>
    <h2 v-else style="color: red">
        На данный момент ещё не были внесены в базу данных
    </h2>`,
    props: {
        instances: {
            type: Array,
            required: true,
        },
        active_instance: {
            type: Object,
            required: true,
        }
    },
    components: {
        'instance-item': instanceItem,
    },
};

const instanceInfo = {
    name: "instance-info",
    template: `
    <div class="instanceInfo">
        <table class="tableSheet">
            <tr>
                <th>Номер:</th>
                <td>{{active_instance.id}}</td>
            </tr>
            <tr>
                <th>
                    Название:
                </th>
                <td>
                    {{active_instance.title}}
                </td>
            </tr>
            <tr>
                <th>
                    Описание:
                </th>
                <td>
                    {{active_instance.body}}
                    {{active_instance.description}}
                </td>
            </tr>
        </table>
    </div>
    `,
    props: {
        active_instance: Object
    }
};

const instanceSheet = {
    name: "instance-sheet",
    template:
        `
        <div class="instanceSheet">
            <div class="row">
                <instance-list class="col-6"
                               :instances="instances"
                               :active_instance="activeInstance"
                               @update:activeInstance="activeInstance">
                </instance-list>
                <instance-info 
                               class="col-6"
                               v-model:active_instance="activeInstance">
                </instance-info>
            </div>
            <div style="display: flex;">
            <div style="margin-right: auto;"></div>
                <input
                   type="submit"
                   class="myButton"
                   value="Выбрать"
                   @click="updateActiveInstance">
            </div>
        </div>
        `,
    props: {
        instances: {
            type: Array,
            required: true
        },
        active_instance: {
            type: Object,
            required: true,
        },
    },
    components: {
        "instance-list": instanceList,
        "instance-info": instanceInfo,
    },
    data() {
        return {
            activeInstance: {
                type: Object,
                required: true,
            }
        }
    },
    mounted() {
        this.activeInstance = this.active_instance
    },
    methods: {
        updateActiveInstance() {
            this.$emit('update:active_instance', this.activeInstance)
            // Calling parent method to close window.
            //this.$emit('update:show', false)
            this.$parent.hideModalWindow()
        }
    }
};
