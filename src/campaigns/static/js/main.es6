import React from 'react/addons';
import { ContextFactory, Action, Store } from 'geiger';

// The Context component (think "Dependency Injection Container")
const Context = ContextFactory({
    todostore: React.PropTypes.object.isRequired,
    todoactions: React.PropTypes.object.isRequired
});

$(document).ready(function() { alert("Hallo 123456789"); });
