## Bottery Nightly

_Changes to be released_

#### Enhancements

- Handler instances returns the selected view ([#161](https://github.com/rougeth/bottery/issues/161))
- Move Telegram and Messenger modules to outside `platform` module. Also rename `platform` module to `platforms` (due to Python builtin `platform` module) ([#161](https://github.com/rougeth/bottery/issues/165))
- Create option to change msg handlers module ([#172](https://github.com/rougeth/bottery/issues/172))
- Remove unused `settings_module` option from Bottery ([#173](https://github.com/rougeth/bottery/issues/173))

#### Bug fixes

- Stop responding with `null` when a view doesn't return anything ([#154](https://github.com/rougeth/bottery/issues/154))

#### Docs

- Simplify Github templates ([#157](https://github.com/rougeth/bottery/issues/157))


## Bottery 0.1.1 (2018-04-28)

#### Features

- Add Middlewares to message/response process ([#155](https://github.com/rougeth/bottery/issues/155)).

#### Docs

- Add Github templates for issues and pull requests ([#151](https://github.com/rougeth/bottery/issues/151)).


## Bottery 0.1.0 (2018-04-22)

#### Features

- Telegram support with polling and webhook modes.
- Telegram widgets for replying and keyboard message.
- Facebook Messenger support.
- Create Handlers (message, startswith, regex and default).
- Create function for template rendering.
