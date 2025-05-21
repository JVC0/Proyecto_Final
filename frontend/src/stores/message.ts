import { defineStore } from 'pinia';

export const useMessageStore = defineStore('message', {
    state: () => ({
        message: '',
        isError: false,
        timeoutId: null as number | null,
    }),
    actions: {
        setMessage(message: string, isError = false) {
            if (this.timeoutId) {
                clearTimeout(this.timeoutId);
            }
            this.message = message;
            this.isError = isError;
            this.timeoutId = setTimeout(() => {
                this.clearMessage();
                this.timeoutId = null;
            }, 50000);
        },
        clearMessage() {
            this.message = '';
            this.isError = false;
            if (this.timeoutId) {
                clearTimeout(this.timeoutId);
                this.timeoutId = null;
            }
        },
    },
});