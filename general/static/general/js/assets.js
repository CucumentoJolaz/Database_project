const modalTemplate = {
    name: "modal-template",
    template: `<div class="dialog"
                    v-if="modalwindowvisible"
                    @click="hideModalWindow">
            <div @click.stop class="dialog__content">
               <slot></slot>
            </div>
        </div>`,
    props: {
        modalwindowvisible: {
            type: Boolean,
            default: false
        }
    },
    methods: {
        hideModalWindow() {
            this.$emit('update:modalwindowvisible', false)
        }
    },
};