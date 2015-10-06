'use strict';

import React from 'react/addons';

export default class TodoList extends React.Component {

    // declaring dependencies to inject; can be a subset of all the context
    static contextTypes = {
        todostore: React.PropTypes.object.isRequired,
        todoactions: React.PropTypes.object.isRequired
    };

    // watching store changes
    componentWillMount() {
        this.unwatch = [this.context.todostore.watch(this.forceUpdate.bind(this))];
    }

    // unwatching store changes
    componentWillUnmount() { this.unwatch.map(cbk => cbk()); }

    render() {
        const { todostore, todoactions } = this.context;

        return (
            <div>
                <h2>Todos</h2>

                <button onClick={() => todoactions.add('Another thing to do !')}>Add todo</button>

                <ul>
                    {todostore.getAll().map(todo => <li>{todo}</li>)}
                </ul>
            </div>
        );
    }
}