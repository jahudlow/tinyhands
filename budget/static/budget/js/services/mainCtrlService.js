angular
    .module('BudgetCalculation')
    .factory('mainCtrlService', mainCtrlService);

mainCtrlService.$inject = ['$http'];

function mainCtrlService($http) {
    return {
        createForm: createForm,
        deletePost: deletePost,
        retrieveNewForm: retrieveNewForm,
        retrieveForm: retrieveForm,
        updateForm: updateForm
	};

    function createForm(form) {
        return $http.post('/budget/api/budget_calculations/', form)
            .success(function(data) {
                return data;
            })
            .error(function(data, status) {
                console.log(data, status);
            });
    }

    function deletePost(id) {
        return $http.delete('/budget/api/budget_calculations/' + id + '/').
            success(function (data, status, headers, config) {
            }).
            error(function (data, status, headers, config) {
            })
    }

    function retrieveNewForm() { // TODO: make this respond to the month_year selector at the top of the page
        return $http.get('/budget/api/budget_calculations/most_recent_form/' + window.budget_calc_id + '/').
            success(function (data) {
                return data;
            }).
            error(function (data, status) {
                console.log(data, status);
            });
    }

    function retrieveForm(id) {
        return $http.get('/budget/api/budget_calculations/' + id + '/').
            success(function (data) {
                return data;
            }).
            error(function (data, status) {
                console.log(data, status);
            });
    }

    function updateForm(id, form) {
        return $http.put('/budget/api/budget_calculations/' + id + '/', form)
            .success(function(data) {
                return data;
            })
            .error(function(data, status) {
                console.log(data, status);
            });
    }
}