angular.module("services", [])
    .factory('sharedModel', function () {
    var sharedModel = {
        basic_done: false,
        perks_done: false,
        duration_done: false,
        title: '',
        description: '',
        perks: []
    };

    return sharedModel;
});