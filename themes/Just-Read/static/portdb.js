
// axios get from here: https://reactgo.com/vue-fetch-data/


var searchapp = new Vue({
    delimiters: ['|', '|'],
    el: '#searchmeta',
    data: {
        ports: [
        "loading",
        ],
        portFilter: '',
    },
    created () {
        this.updateData();
    },
    computed: {
        portFiltered() {
            if (this.portFilter!="") {
                return this.ports.filter(port => {
                    const matchTerm = port.message.toLowerCase();
                    const search = this.portFilter.toLowerCase();
                    return matchTerm.includes(search)
                });
            } else {
            return []
            }
        },
    },
    methods: {
        updateData: function() {
            axios
            .get("/theme/searchdata.json", headers={'crossDomain': true})
            .then(res => {
                // console.log(res);
                let data = res.data.map(function(el) {
                    // console.log({ "message" : el.toLowerCase() });
                    return { "message" : el.toLowerCase() };
                });
                this.ports = data;
            });
        }
    }
})

