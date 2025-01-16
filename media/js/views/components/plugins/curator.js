define([
    'knockout',
    'arches',
    'js-cookie',
    'templates/views/components/plugins/curator.htm'
], function(ko, arches, Cookies, CuratorTemplate) {

    const CuratorViewModel = function() {
        const self = this;
        this.loading = ko.observable(true);
        this.records = ko.observable();

        this.getStatus = async function() {
            const response = await window.fetch("/curator");
            const data = await response.json();
            self.records(data.records);
            self.loading(false);
        };

        this.saveStatus = async function() {
            const response = await fetch("/curator", {
                method: 'POST',
                credentials: 'include',
                headers: {
                    "X-CSRFToken": Cookies.get('csrftoken')
                }
            });
            const data = await response.json();
            self.records(data.records);
        };

        this.getStatus();
    };

    return ko.components.register('curator', {
        viewModel: CuratorViewModel,
        template: CuratorTemplate
    });
});
