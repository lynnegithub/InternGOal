(function () {
	'use strict';

	angular
		.module('interngoal.authentication', [
			'interngoal.authentication.controllers',
			'interngoal.authentication.services'
		]);

	angular
		.module('interngoal.authentication.controllers', []);

	angular
		.module('interngoal.authentication.services', ['ngCookies']);
})();