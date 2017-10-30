# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import itertools
import operator
import os.path

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles

from openstack_releases import deliverable
from openstack_releases import links


def _list_table(add, headers, data, title='', columns=None):
    """Build a list-table directive.

    :param add: Function to add one row to output.
    :param headers: List of header values.
    :param data: Iterable of row data, yielding lists or tuples with rows.
    """
    add('.. list-table:: %s' % title)
    add('   :header-rows: 1')
    if columns:
        add('   :widths: %s' % (','.join(str(c) for c in columns)))
    add('')
    add('   - * %s' % headers[0])
    for h in headers[1:]:
        add('     * %s' % h)
    for row in data:
        add('   - * %s' % row[0])
        for r in row[1:]:
            lines = str(r).splitlines()
            if not lines:
                # empty string
                add('     * ')
            else:
                # potentially multi-line string
                add('     * %s' % lines[0])
                for l in lines[1:]:
                    add('       %s' % l)
    add('')


def _get_category(data):
    model = data.get('release-model')
    if model == 'cycle-trailing':
        return 'cycle-trailing'
    return data.get('type', 'other')


_deliverables = None


def _initialize_deliverable_data(app):
    global _deliverables

    _deliverables = deliverable.Deliverables('deliverables')


class DeliverableDirectiveBase(rst.Directive):

    option_spec = {
        'series': directives.unchanged,
        'team': directives.unchanged,
    }

    _CATEGORY_ORDER = [
        'service',
        'library',
        'horizon-plugin',
        'other',
        'cycle-trailing',
    ]

    def run(self):
        env = self.state.document.settings.env
        app = env.app

        # The series value is optional for some directives. If it is
        # present but an empty string, convert to None so the
        # Deliverables class will treat it like a wildcard.
        series = self.options.get('series') or None

        # If the user specifies a team, track only the deliverables
        # for that team.
        self.team_name = self.options.get('team') or None

        result = ViewList()

        # Assemble all of the deliverable data to be displayed and
        # build the RST representation.

        # get_deliverables() -> (team, series, deliverable, info)

        if self.team_name:
            # All deliverables are shown, in alphabetical order. They
            # are organized by series but not type.
            d_source = itertools.groupby(
                sorted(_deliverables.get_deliverables(self.team_name, series)),
                key=operator.itemgetter(1)  # the series
            )
            for s, d in d_source:
                self._add_deliverables(
                    None,
                    ((i[2], i[3]) for i in d),  # only name and info
                    s,
                    app,
                    result,
                )
        else:
            # Only the deliverables for the given series are
            # shown. They are categorized by type, which we need to
            # extract from the data.
            raw_deliverables = [
                (_get_category(_data), _deliv_name, _data)
                for _team, _series, _deliv_name, _data in _deliverables.get_deliverables(
                    self.team_name,
                    series,
                )
            ]
            grouped = itertools.groupby(
                sorted(raw_deliverables),
                key=operator.itemgetter(0),  # the category
            )
            # Convert the grouping iterators to a dictionary mapping
            # type to the list of tuples with deliverable name and
            # parsed deliverable info that _add_deliverables() needs.
            by_category = {}
            for deliverable_category, deliverables in grouped:
                by_category[deliverable_category] = [
                    (d[1], d[2])
                    for d in deliverables
                ]
            for category in self._CATEGORY_ORDER:
                if category not in by_category:
                    app.info('No %r for %s' % (category, (self.team_name, series)))
                    continue
                self._add_deliverables(
                    category,
                    by_category[category],
                    series,
                    app,
                    result,
                )

        # NOTE(dhellmann): Useful for debugging.
        # print('\n'.join(result))

        node = nodes.section()
        node.document = self.state.document
        nested_parse_with_titles(self.state, result, node)
        return node.children

    _TYPE_TITLE = {
        'service': 'Service Projects',
        'horizon-plugin': 'Horizon Plugins',
        'library': 'Library Projects',
        'other': 'Other Projects',
        'cycle-trailing': 'Projects Trailing the Release Cycle',
    }

    def _add_deliverables(self, type_tag, deliverables, series, app, result):
        source_name = '<' + __name__ + '>'

        # expand any generators passed in and filter out deliverables
        # with no releases
        deliverables = list(
            d
            for d in deliverables
            if d[1].get('releases')
        )
        if not deliverables:
            # There are no deliverables of this type, and that's OK.
            return

        result.append('', source_name)
        if type_tag is not None:
            title = self._TYPE_TITLE.get(type_tag, 'Unknown Projects')
            result.append('-' * len(title), source_name)
            result.append(title, source_name)
            result.append('-' * len(title), source_name)
            result.append('', source_name)

        # Build a table of the first and most recent versions of each
        # deliverable.
        if not self.team_name:
            most_recent = []
            for deliverable_name, deliverable_info in deliverables:
                earliest_version = deliverable_info.get('releases', {})[0].get(
                    'version', 'unreleased')
                recent_version = deliverable_info.get('releases', {})[-1].get(
                    'version', 'unreleased')
                ref = ':ref:`%s-%s`' % (series, deliverable_name)
                release_notes = deliverable_info.get('release-notes')
                if not release_notes:
                    notes_link = ''
                elif isinstance(release_notes, dict):
                    notes_link = '\n'.join(
                        '| `%s release notes <%s>`__' % (n.split('/')[-1], v)
                        for n, v in sorted(release_notes.items())
                    )
                else:
                    notes_link = '`release notes <%s>`__' % release_notes
                most_recent.append(
                    (ref, earliest_version, recent_version, notes_link)
                )
            _list_table(
                lambda t: result.append(t, source_name),
                ['Deliverable', 'Earliest Version',
                 'Most Recent Version', 'Notes'],
                most_recent,
                title='Release Summary',
            )

        # Show the detailed history of the deliverables within the series.

        for deliverable_name, deliverable_info in deliverables:

            # These closures need to be redefined in each iteration of
            # the loop because they use the deliverable name.
            def _add(text):
                result.append(text, '%s/%s' % (series, deliverable_name))

            def _title(text, underline):
                text = str(text)  # version numbers might be seen as floats
                if self.team_name:
                    _add('.. _team-%s-%s:' % (series, text))
                else:
                    _add('.. _%s-%s:' % (series, text))
                _add('')
                _add(text)
                _add(underline * len(text))
                _add('')

            _title(deliverable_name, '=')

            app.info('[deliverables] rendering %s (%s)' %
                     (deliverable_name, series))

            release_notes = deliverable_info.get('release-notes')
            if not release_notes:
                notes_link = None
            elif isinstance(release_notes, dict):
                notes_link = ' | '.join(
                    '`%s <%s>`__' % (n.split('/')[-1], v)
                    for n, v in sorted(release_notes.items())
                )
            else:
                notes_link = '`%s <%s>`__' % (deliverable_name, release_notes)
            if notes_link:
                _add('')
                _add('Release Notes: %s' % notes_link)
                _add('')
            # We have signatures for artifacts only after newton
            if series and series[0] >= 'o':
                headers = ['Version', 'Signature', 'Repo', 'Git Commit']
                data = ((links.artifact_link(r['version'], p,
                                             deliverable_info),
                         links.artifact_signature_link(r['version'],
                                                       'pgp', p,
                                                       deliverable_info),
                         p['repo'], p['hash'])
                        for r in reversed(deliverable_info.get('releases', []))
                        for p in r.get('projects', []))
                columns = [10, 10, 40, 50]
            else:
                headers = ['Version', 'Repo', 'Git Commit']
                data = ((links.artifact_link(r['version'], p,
                                             deliverable_info),
                         p['repo'], p['hash'])
                        for r in reversed(deliverable_info.get('releases', []))
                        for p in r.get('projects', []))
                columns = [10, 40, 50]
            _list_table(
                _add,
                headers=headers,
                data=data,
                columns=columns,
            )


class DeliverableDirective(DeliverableDirectiveBase):

    def run(self):
        # Require a series value.
        series = self.options.get('series')
        if not series:
            error = self.state_machine.reporter.error(
                'No series set for deliverable directive',
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        return super(DeliverableDirective, self).run()


class IndependentDeliverablesDirective(DeliverableDirectiveBase):
    pass


class TeamDirective(rst.Directive):

    option_spec = {
        'series': directives.unchanged,
        'name': directives.unchanged,
    }

    def run(self):
        # If the user specifies a team, track only the deliverables
        # for that team.
        self.team_name = self.options.get('name')
        if not self.team_name:
            error = self.state_machine.reporter.error(
                'No team name in team directive',
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        self.team_deliverables = _deliverables.get_team_deliverables(
            self.team_name
        )

        all_series = reversed(sorted(
            _deliverables.get_team_series(self.team_name)
        ))

        result = ViewList()

        def _add(text):
            result.append(text, '<team tag>')

        for series in all_series:
            series_title = series.lstrip('_').title()
            _add(series_title)
            _add('=' * len(series_title))
            _add('')
            _add('.. deliverable::')
            _add('   :series: %s' % series)
            _add('   :team: %s' % self.team_name)
            _add('')

        # NOTE(dhellmann): Useful for debugging.
        # print('\n'.join(result))

        node = nodes.section()
        node.document = self.state.document
        nested_parse_with_titles(self.state, result, node)
        return node.children


def _generate_team_pages(app):
    teams_with_deliverables = list(sorted(_deliverables.get_teams()))
    for team_name in teams_with_deliverables:
        app.info('[team page] %s' % team_name)
        slug = team_name.lower().replace('-', '_').replace(' ', '_')
        base_file = slug + '.rst'
        with open(os.path.join('doc/source/teams', base_file), 'w') as f:
            f.write('=' * (len(team_name) + 2))
            f.write('\n')
            f.write(' %s\n' % team_name.title())
            f.write('=' * (len(team_name) + 2))
            f.write('\n\n')
            f.write('.. team::\n')
            f.write('   :name: %s\n' % team_name)
    return


class HighlightsDirective(rst.Directive):
    """Directive to pull series highlights into docs output."""

    option_spec = {
        'series': directives.unchanged,
    }

    def _get_deliverable_highlights(self, series):
        """Collects the highlights for the series.

        :param series: The series to extract highlights from.
        :returns: The available highlights for the series.
        """
        series_highlights = {}
        series_deliverables = _deliverables.get_deliverables(None, series)
        for deliv in series_deliverables:
            series_info = deliv[3]
            highlights = series_info.get('cycle-highlights')
            if highlights:
                # Add highlights to any existing notes already collected
                notes = series_highlights.get(series_info['team'])
                series_highlights[series_info['team']] = '{}{}\n\n'.format(
                    notes, highlights)

        return series_highlights

    def run(self):
        env = self.state.document.settings.env
        app = env.app

        # Get the series we are reporting on
        series = self.options.get('series')
        if not series:
            raise self.error('series value must be set to a valid cycle name.')

        result = ViewList()
        series_highlights = self._get_deliverable_highlights(series)
        source_name = '<{}>'.format(__name__)

        for team in series_highlights.keys():
            app.info('[highlights] rendering %s highlights for %s' %
                     (team.title(), series))

            result.append(team.title(), source_name)
            result.append('-' * len(team), source_name)
            result.append(series_highlights[team], source_name)
            result.append('', source_name)

        node = nodes.section()
        node.document = self.state.document
        nested_parse_with_titles(self.state, result, node)
        return node.children


def setup(app):
    _initialize_deliverable_data(app)
    app.add_directive('deliverable', DeliverableDirective)
    app.add_directive('independent-deliverables',
                      IndependentDeliverablesDirective)
    app.add_directive('team', TeamDirective)
    app.add_directive('serieshighlights', HighlightsDirective)
    _generate_team_pages(app)
