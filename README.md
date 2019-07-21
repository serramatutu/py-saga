# py-saga
py-saga is an open-source python implementation of the [saga](https://microservices.io/patterns/data/saga.html) pattern.

## What are Sagas?
[Sagas](https://microservices.io/patterns/data/saga.html) are a way to execute complex transactions across distributed systems while guaranteeing [eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency).

In short, they are transactions made up of possibly interdependent steps. Those steps are executed in paralell across a distributed system. If one of them fails, all other steps are undone through a _compensation_.

For example: imagine you have a scenario where a user is trying to purchase a trip package to Rio. This package includes roundtrip airplane tickets, a hotel booking and tickets for the [Christ the Redeemer statue](https://en.wikipedia.org/wiki/Christ_the_Redeemer_(statue)).

In this case, your _buy package_ saga is composed of three different steps:
- book plane ticket
- book hotel room
- buy tourist tickets

In case any of those steps fails, you must undo the other ones, because the package can only be sold as a unit. For this reason, you also have to define _compensations_ for each step. Your steps then look like this:

| Step                | Compensation                  |
| ------------------- | ----------------------------- |
| book plane ticket   | cancel plane ticket booking   |
| book hotel room     | cancel hotel room reservation |
| buy tourist tickets | cancel ticket reservation     |

Let's execute our _buy package_ saga then!

When Maria tries to buy her package, everything goes according to plan, and the saga is executed as planned:
```
❗️️ begin saga

✔️ book plane ticket
✔️ book hotel room
✔️ buy tourist tickets

❗️️ all steps succeeded

️✔️ end saga (success)
```

However, when Kevin tries to buy his packages, the hotel informs there aren't any available rooms. The saga is then executed as follows:
```
❗️️ begin saga

✔️ book plane ticket
❌ book hotel room (no available hotel rooms)
✔️ buy tourist tickets

❗️️ step failed: reverting

✔ ️cancel plane ticket booking
✔ cancel tourist ticket reservations

❌ end saga (no available hotel rooms)
```

Notice that, for both cases, the final system state is coherent, even though in one case our distributed transaction failed.