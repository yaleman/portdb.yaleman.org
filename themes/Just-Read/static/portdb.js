
// axios get from here: https://reactgo.com/vue-fetch-data/


var searchapp = new Vue({
    delimiters: ['|', '|'],
    el: '#searchmeta',
    data: {
        ports: [
            { message: "loading"},
        ],
        portFilter: '',
        category: '',
    },
    created () {
        this.updateData();

        // console.log("about to log category");
        // console.log(this.category);
        // console.log("done logging category");
    },
    computed: {
        portFiltered() {
            if (this.portFilter!="" &&  this.getCategory() == "" ) {
                // search box
                const search = this.portFilter.toLowerCase();
                return this.ports.filter(port => {
                    const portToMatch = port.message.toLowerCase();
                    return portToMatch.includes(search);
                }).reverse();
            } else if ( this.getCategory() != "" && this.portFilter == "" ) {
                return this.ports.filter(port => {
                    const portToMatch = port.message.toLowerCase();
                    return portToMatch.includes(this.getCategory());
                }).reverse();

            } else if (  this.getCategory() != "" && this.portFilter != "" ) {
                return this.ports.filter(port => {
                    const portToMatch = port.message.toLowerCase();

                    return portToMatch.includes(this.getCategory()) && portToMatch.includes(this.portFilter);
                }).reverse();

            }

            return [];
        },
    },
    methods: {
        getCategory: function() {
            const result = this.$el.getAttribute("data-category");

            if (result != undefined) {
                return result;
            }
            return "";
        },
        updateData: function() {
            axios
            .get("/theme/searchdata.json", headers={'crossDomain': true})
            .then(res => {
                // console.log(res);
                let data = res.data.map(function(el) {
                    // console.log({ "message" : el.toLowerCase() });
                    return { "message" : el.toLowerCase() };
                });
                this.ports = data.reverse();
            });
        }
    }
})

