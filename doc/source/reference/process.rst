===================
 Release Processes
===================

This document describes the process and week-per-week steps related to
preparing the release. It should be adapted to take team holidays and
other commitments into account, and turned into a clear action plan for
the release cycle.

Week after previous release
===========================

#. Process any late or blocked release requests for deliverables
   for any branch (treating the new series branch as stable).

#. Prepare for the next release cycle by adding deliverable files under the
   next cycle's directory. Remove any deliverable files from the current cycle
   that ended up not having any releases. Then run the following command to use
   the current cycle deliverables to generate placeholders for the next cycle::

      tox -e venv -- init-series $SERIES $NEXT_SERIES

#. Coordinate with the Infrastructure team to swap out the previous cycle
   signing key and establish the new one for the startniog cycle.

#. Create the $series-relmgt-tracking etherpad using the
   ``make-tracking-etherpad`` command.
   For example::

       tox -e venv -- make-tracking-pad ussuri

   The output from this command can be pasted into a
   ``$SERIES-relmgt-tracking`` etherpad. Set title formatting for the top
   sections. Then highlight all listed weeks and set to **Heading 3** style.
   Fill in the contents of one of the weeks with the typical items, then copy
   and past that into each subsequent week to prepare for the rest of the
   cycle.

#. Email PTLs directly one time to explain the use of the "[release][ptl]"
   email tag on the openstack-discuss list and tell them to pay attention
   to [release] countdown emails.

#. At the end of the week, send the following weekly email content::

    Welcome back to the release countdown emails! These will be sent at
    major points in the $SERIES development cycle, which should conclude
    with a final release on $release-date.

    Development Focus
    -----------------

    At this stage in the release cycle, focus should be on planning the
    $SERIES development cycle, assessing $SERIES community goals and approving
    $SERIES specs.

    General Information
    -------------------

    $remark-on-series-length. In case you haven't seen it yet, please take
    a look over the schedule for this release:

    https://releases.openstack.org/$SERIES/schedule.html

    By default, the team PTL is responsible for handling the release cycle
    and approving release requests. This task can (and probably should) be
    delegated to release liaisons. Now is a good time to review release
    liaison information for your team and make sure it is up to date:

    https://opendev.org/openstack/releases/src/branch/master/data/release_liaisons.yaml

    By default, all your team deliverables from the Train release are
    continued in $SERIES with a similar release model. If you intend to drop
    a deliverable, or modify its release model, please do so before the
    $SERIES-1 milestone by proposing a change to the deliverable file at:

    https://opendev.org/openstack/releases/src/branch/master/deliverables/$SERIES

    Upcoming Deadlines & Dates
    --------------------------

    $other-upcoming-event_
    $SERIES-1 milestone: $milestone1


Week before milestone-1
=======================

#. Review cycle-trailing projects to check which haven't released yet.
   Ask them to prepare their releases, if they haven't already. The list
   of pending cycle-trailing deliverables can be determined by running
   the command::

     tox -e venv -- list-deliverables --series $LASTSERIES \
         --model cycle-trailing --missing-final

#. At the end of the week, send the following weekly email content::

    Development Focus
    -----------------

    The $SERIES-1 milestone is next week, on $milestone1! Project team plans
    for the $SERIES cycle should now be solidified.

    General Information
    -------------------

    If you planned to change the release model for any of your deliverables
    this cycle, please remember to do so ASAP, before milestone-1.

    Libraries need to be released at least once per milestone period. Next
    week, the release team will propose releases for any library which had
    changes but has not been otherwise released since the $LASTSERIES release.
    PTL's or release liaisons, please watch for these and give a +1 to
    acknowledge them. If there is some reason to hold off on a release, let
    us know that as well, by posting a -1. If we do not hear anything at all
    by the end of the week, we will assume things are OK to proceed.

    NB: If one of your libraries is still releasing 0.x versions, start
    thinking about when it will be appropriate to do a 1.0 version. The
    version number does signal the state, real or perceived, of the library,
    so we strongly encourage going to a full major version once things are
    in a good and usable state.

    Upcoming Deadlines & Dates
    --------------------------

    $SERIES-1 milestone: $milestone1


Milestone-1
===========

#. Propose autoreleases for cycle-with-intermediary libraries which
   did not release since the previous release.

   - List them using::

       tox -e venv -- list-deliverables --unreleased \
       --model cycle-with-intermediary --type client-library --type library

   - Generate release requests for all cycle-with-intermediary libraries
     which had changes, but did not release since the previous release.
     That patch will be used as a base to communicate with the team: if
     a team wants to wait for a specific patch to make it to the library,
     someone from the team can -1 the patch to have it held, or update
     that patch with a different commit SHA.

   - Between Tuesday and Thursday, merge as soon as possible the patches that
     get +1 from the PTL or the release liaison.

   - On the Friday, merge patches that did not get any feedback from PTL or
     release liaison. Discuss standing -1s to see if they should be granted
     an exception and wait until next week.

#. To catch if there are acl issues in newly created repositories,
   run tools/aclissues.py to detect potential leftovers in Gerrit ACLs
   allowing official deliverables to be directly tagged or branched without
   going through openstack/releases. You need to specify the location
   of up-to-date checkouts for the governance and the project-config
   repositories. For example::

     tools/aclissues.py ../project-config ../governance

   If the tool reports any violation, you can re-run it with ``--patch`` to
   generate needed changes in ../project-config to align ACLs with governance,
   and propose the changes for review.

#. At the end of the week, send the following weekly email content::

    Development Focus
    -----------------

    We are now past the $SERIES-1 milestone. Teams should now be focused on
    feature development and completion of release cycle goals [0].

    [0] https://governance.openstack.org/tc/goals/selected/$SERIES/index.html

    General Information
    -------------------

    Our next milestone in this development cycle will be $SERIES-2, on
    $milestone2. This milestone is when we freeze the list of deliverables
    that will be included in the $SERIES final release, so if you plan to
    introduce new deliverables in this release, please propose a change to
    add an empty deliverable file in the deliverables/$SERIES directory of
    the openstack/releases repository.

    Now is also generally a good time to look at bugfixes that were
    introduced in the master branch that might make sense to be backported
    and released in a stable release.

    If you have any question around the OpenStack release process, feel free
    to ask on this mailing-list or on the #openstack-release channel on IRC.

    Upcoming Deadlines & Dates
    --------------------------

    $SERIES-2 Milestone: $milestone2


Week after milestone-1
======================

#. Review any remaining milestone-1 exceptions


Between Milestone-1 and Milestone-2
===================================

#. Send the following weekly email content::

    Development Focus
    -----------------

    The $SERIES-2 milestone will happen in next month, on $milestone2.
    $SERIES-related specs should now be finalized so that teams can move
    to implementation ASAP. Some teams observe specific deadlines on
    the second milestone (mostly spec freezes): please refer to
    https://releases.openstack.org/$SERIES/schedule.html for details.

    General Information
    -------------------

    Please remember that libraries need to be released at least once per
    milestone period. At milestone 2, the release team will propose releases
    for any library that has not been otherwise released since milestone 1.

    Other non-library deliverables that follow the cycle-with-intermediary
    release model should have an intermediary release before milestone-2.
    Those who haven't will be proposed to switch to the cycle-with-rc model,
    which is more suited to deliverables that are released only once per cycle.

    At milestone-2 we also freeze the contents of the final release. If you
    have a new deliverable that should be included in the final release, you
    should make sure it has a deliverable file in:
    https://opendev.org/openstack/releases/src/branch/master/deliverables/$series
    You should request a beta release (or intermediary release) for those new
    deliverables by milestone-2. We understand some may not be quite ready
    for a full release yet, but if you have something minimally viable to
    get released it would be good to do a 0.x release to exercise the release
    tooling for your deliverables. See the MembershipFreeze description for
    more details: https://releases.openstack.org/$SERIES/schedule.html#$S-mf

    Finally, now may be a good time for teams to check on any stable
    releases that need to be done for your deliverables. If you have
    bugfixes that have been backported, but no stable release getting
    those. If you are unsure what is out there committed but not released,
    in the openstack/releases repo, running the command
    "tools/list_stable_unreleased_changes.sh <cycle_name>" gives a nice report.

    Upcoming Deadlines & Dates
    --------------------------

    $SERIES-2 Milestone: $milestone2


Week before Milestone-2
=======================

#. Ahead of MembershipFreeze, run ``membership_freeze_test`` to check for
   any new deliverable in governance that has not been released yet::

     tox -e membership_freeze_test -- $series ~/branches/governance/reference/projects.yaml

   Those should either be tagged as a release management exception if they do
   not need to be released (see ``release-management`` key in the governance
   projects.yaml file) or an empty deliverable file should be added to the
   series so that we can properly track it. Leftovers are considered too young
   to be released in the next release and will be reconsidered at the next
   cycle.

#. Send the following weekly email content::

    Development Focus
    -----------------

    The $SERIES-2 milestone is next week, on $milestone2! $SERIES-related
    specs should now be finalized so that teams can move to implementation
    ASAP. Some teams observe specific deadlines on the second milestone
    (mostly spec freezes): please refer to
    https://releases.openstack.org/$SERIES/schedule.html for details.

    General Information
    -------------------

    Libraries need to be released at least once per milestone period. Next
    week, the release team will propose releases for any library that has not
    been otherwise released since milestone 1. PTL's and release liaisons,
    please watch for these and give a +1 to acknowledge them. If there is
    some reason to hold off on a release, let us know that as well. A +1
    would be appreciated, but if we do not hear anything at all by the end
    of the week, we will assume things are OK to proceed.

    Remember that non-library deliverables that follow the
    cycle-with-intermediary release model should have an intermediary
    release before milestone-2. Those who haven't will be proposed to switch
    to the cycle-with-rc model, which is more suited to deliverables that
    are released only once per cycle.

    Next week is also the deadline to freeze the contents of the final
    release. All new '$SERIES' deliverables need to have a deliverable file
    in https://opendev.org/openstack/releases/src/branch/master/deliverables
    and need to have done a release by milestone-2. The following new
    deliverables have not had a release yet, and will not be included in
    $SERIES unless a release is requested for them in the coming week:

    [ list of deliverables ]

    Changes proposing those deliverables for inclusion in $SERIES have been
    posted, please update them with an actual release request before the
    milestone-2 deadline if you plan on including that deliverable in $SERIES,
    or -1 if you need one more cycle to be ready.

    Upcoming Deadlines & Dates
    --------------------------

    $SERIES-2 Milestone: $milestone2


Milestone-2
===========

#. Generate a list of all cycle-with-intermediary libraries which did not
   release since the YYYY-MM-DD date of milestone-1. For this, run::

     tox -e venv -- list-deliverables --unreleased-since YYYY-MM-DD
     --model cycle-with-intermediary --type client-library --type library

   Generate release requests for all cycle-with-intermediary libraries
   which had changes, but did not release since milestone-1.
   That patch will be used as a base to communicate with the team:
   if a team wants to wait for a specific patch to make it to the library,
   someone from the team can -1 the patch to have it held, or update
   that patch with a different commit SHA.

#. To catch if there are acl issues in newly created repositories,
   run ``tools/aclissues.py`` to detect potential leftovers in Gerrit ACLs
   allowing official deliverables to be directly tagged or branched without
   going through openstack/releases. You need to specify the location
   of up-to-date checkouts for the governance and the project-config
   repositories. For example::

     tools/aclissues.py ../project-config ../governance

   If the tool reports any violation, you can re-run it with ``--patch`` to
   generate needed changes in ../project-config to align ACLs with governance,
   and propose the changes for review.

#. Send the following weekly email content::

    Development Focus
    -----------------

    We are now past the $SERIES-2 milestone, and entering the last development
    phase of the cycle. Teams should be focused on implementing planned work
    for the cycle.

    Now is a good time to review those plans and reprioritize anything if
    needed based on the what progress has been made and what looks realistic
    to complete in the next few weeks.

    General Information
    -------------------

    Looking ahead to the end of the release cycle, please be aware of the
    feature freeze dates. Those vary depending on deliverable type:

    * General libraries (except client libraries) need to have their last
      feature release before Non-client library freeze ($nclfreeze). Their
      stable branches are cut early.

    * Client libraries (think python-*client libraries) need to have their
      last feature release before Client library freeze ($milestone3)

    * Deliverables following a cycle-with-rc model (that would be most
      services) observe a Feature freeze on that same date, $milestone3.
      Any feature addition beyond that date should be discussed on the
      mailing-list and get PTL approval. After feature freeze, cycle-with-rc
      deliverables need to produce a first release candidate (and a stable
      branch) before RC1 deadline ($rc1-deadline)

    * Deliverables following cycle-with-intermediary model can release as
      necessary, but in all cases before Final RC deadline ($final-rc-deadline)

    Upcoming Deadlines & Dates
    --------------------------

    Non-client library freeze: $nclfreeze (R-6 week)
    Client library freeze: $milestone3 (R-5 week)
    Ussuri-3 milestone: $milestone3 (R-5 week)
    $other-upcoming-event


Between Milestone-2 and Milestone-3
===================================

#. Plan the next release cycle schedule based on the number of desired weeks or
   by making sure the cycle ends within a few weeks of the next developer
   event. Using the Monday of the close of the last cycle, and the
   Monday of the planned last week of the new cycle, use the tool
   ``tools/list_weeks.py`` to generate the release schedule YAML file.
   For example::

        ./tools/list_weeks.py t 2019-04-15 2019-10-16

   The generated output can be used to set up the schedule similar to what was
   done for the `Ussuri release <https://review.opendev.org/#/c/679822/>`_.

#. In the countdown email immediately after Milestone-2, include a
   reminder about the various freezes that happen around Milestone-3.

   Remind PTLs a heads up to start thinking about what they might want to
   include in their deliverables file as cycle-highlights
   and that feature freeze is the deadline for them.

#. Check with the election team about whether the countdown email
   needs to include any updates about the election schedule.

#. Generate a list of intermediary-released service deliverables that have
   not done a release in this cycle yet. For this, use::

     tox -e venv -- list-deliverables --unreleased \
     --model cycle-with-intermediary \
     --type horizon-plugin --type other --type service

   Intermediary-released deliverables that did release only once during
   the last cycle, and have not done a release yet are good candidates to
   switch to the cycle-with-rc model, which is much more suitable for
   deliverables that are only released once per cycle.

   Propose a release model change for all deliverables meeting that criteria.
   PTLs and release liaisons may decide to:

   - immediately release an intermediary release (and -1 the proposed change)
   - confirm the release model change (+1 the proposed change)
   - stay uncertain for this cycle of how many releases will be made, but
     acknowledge that they need to do a release before RC1 (-1 the proposed
     change)

#. Two weeks before Milestone-3, include a reminder about the final
   library release freeze coming the week before Milestone-3.

   #. Run the following command to get a list of libraries::

        tools/list_library_unreleased_changes.sh

   #. Include list of unreleased libraries in the email to increase visibility.

#. One week before Milestone-3, include a reminder about the final
   client library release freeze coming the week of Milestone-3.

   #. Run the following command to get a list of client libraries::

        tools/list_client_library_unreleased_changes.sh

   #. Include list of unreleased client libraries in the email to increase
      visibility.

#. Two weeks before Milestone-3, prepare other teams to the final release
   rush.

   #. Ask the release liaisons for the affected teams to audit the
      contents of their ``$project-stable-maint`` groups, as that group
      will control the ``stable/$series`` branch prior to release. They
      should reach out to the ``stable-maint-core`` group for additions.

   #. Include a reminder about the stable branch ACLs in the countdown email.

   #. Notify the Infrastructure team to `generate an artifact signing key`_
      (but not replace the current one yet), and
      begin the attestation process.

      .. _generate an artifact signing key: https://docs.openstack.org/infra/system-config/signing.html#generation

   #. Include a reminder in the weekly countdown email reminding PTLs of the
      feature freeze deadline for cycle-highlights.

R-6 week (Final Library Release deadline)
=========================================

#. Propose autoreleases for cycle-with-intermediary libraries (excluding
   client libraries) which had commits that have not been included in a
   release.

   - List them using::

      ./tools/list_library_unrelease_changes.sh

   - That patch will be used as a base to communicate with the
     team: if a team wants to wait for a specific patch to make it to the
     library, someone from the team can -1 the patch to have it held, or update
     that patch with a different commit SHA.

     .. note::

      At this point, we want *all* changes in the deliverables, to ensure
      that we have CI configuration up to date when the stable branch
      is created later.

   - Allow the ``stable/$series`` branch to be requested with each library
     final release if they know they are ready. Do not require branching at
     this point in case of critical issues requiring another approved release
     past the freeze date.

   - Between Tuesday and Thursday, merge as soon as possible the patches that
     get +1 from the PTL or the release liaison.

   - On the Friday, merge patches that did not get any feedback from PTL or
     release liaison. Discuss standing -1s to see if they should be granted
     an exception and wait until next week.

#. Update the feature list and allowed stable branch names in
   devstack-gate for the new stable branch. For
   example, https://review.opendev.org/362435 and
   https://review.opendev.org/363084

#. At the end of the week, send weekly email content preparing for R-5 week::

    Development Focus
    -----------------

    We are getting close to the end of the $series cycle! Next week on
    $milestone3 is the $series-3 milestone, also known as feature freeze.
    It's time to wrap up feature work in the services and their client
    libraries, and defer features that won't make it to the $next-series cycle.

    General Information
    -------------------

    This coming week is the deadline for client libraries: their last feature
    release needs to happen before "Client library freeze" on $milestone3.
    Only bugfix releases will be allowed beyond this point.

    When requesting those library releases, you can also include the
    stable/$series branching request with the review. As an example, see the
    "branches" section here:
    https://opendev.org/openstack/releases/src/branch/master/deliverables/pike/os-brick.yaml#n2

    $milestone3 is also the deadline for feature work in all OpenStack
    deliverables following the cycle-with-rc model. To help those projects
    produce a first release candidate in time, only bugfixes should be allowed
    in the master branch beyond this point. Any feature work past that deadline
    has to be raised as a Featur Freeze Exception (FFE) and approved by the
    team PTL.

    Finally, feature freeze is also the deadline for submitting a first version
    of your cycle-highlights. Cycle highlights are the raw data hat helps shape
    what is communicated in press releases and other release activity at the
    end of the cycle, avoiding direct contacts from marketing folks. See
    https://docs.openstack.org/project-team-guide/release-management.html#cycle-highlights
    for more details.

    Upcoming Deadlines & Dates
    --------------------------

    $series-3 milestone (feature freeze): $milestone3 (R-5 week)
    RC1 deadline: $rc1-deadline (R-3 week)
    Final RC deadline: $final-rc-deadline (R-1 week)
    Final Train release: $release-date
    $other-upcoming-event


R-5 week (Milestone-3)
======================

#. Process any remaining library freeze exception.

#. Early in the week, email openstack-discuss list to remind PTLs that
   cycle-highlights are due this week so that they can be included in
   release marketing preparations.

#. Propose autoreleases for cycle-with-intermediary client libraries which
   had commits that have not been included in a release.

   - List them using::

      ./tools/list_client_library_unreleased_changes.sh

   - That patch will be used as a base
     to communicate with the team: if a team wants to wait for a specific patch
     to make it to the library, someone from the team can -1 the patch to have
     it held, or update that patch with a different commit SHA.

   - Allow the ``stable/$series`` branch to be requested with each client
     library final release if they know they are ready. Do not require
     branching at this point in case of critical issues requiring another
     approved release past the freeze date.

   - Between Tuesday and Thursday, merge as soon as possible the patches that
     get +1 from the PTL or the release liaison.

   - On the Friday, merge patches that did not get any feedback from PTL or
     release liaison. Discuss standing -1s to see if they should be granted
     an exception and wait until next week.

#. Evaluate any libraries that did not have any change merged over the
   cycle to see if it is time to `transition them to the independent release
   model <https://releases.openstack.org/reference/release_models.html#openstack-related-libraries>`__.

   If it is OK to transition them, propose to move the deliverable file to
   the ``_independent`` directory.

   If it is not OK to transition them, create a new stable branch from the
   latest release from the previous series.

#. List cycle-with-intermediary deliverables that have not been released yet::

     tox -e venv -- list-deliverables --unreleased \
     --model cycle-with-intermediary \
     --type horizon-plugin --type other --type service

   Send a separate email targeted to teams with such unreleased deliverables
   saying::

    Quick reminder that we'll need a release very soon for a number of
    deliverables following a cycle-with-intermediary release model but which
    have not done *any* release yet in the $series cycle:

    {{list-of-deliverables}}

    Those should be released ASAP, and in all cases before $rc1-deadline, so
    that we have a release to include in the final $series release.

#. On Friday, remind the requirements team to freeze changes to
   ``openstack/requirements`` by applying -2 to all
   open patches. Ensure that reviewers do not approve changes created
   by the proposal bot, but do approve changes for new OpenStack deliverable
   releases.

#. At the end of the week, send weekly email content for R-3 week::

    Development Focus
    -----------------

    We just passed feature freeze! Until release branches are cut, you
    should stop accepting featureful changes to deliverables following the
    cycle-with-rc release model, or to libraries. Exceptions should be
    discussed on separate threads on the mailing-list, and feature freeze
    exceptions approved by the team's PTL.

    Focus should be on finding and fixing release-critical bugs, so that
    release candidates and final versions of the $series deliverables can be
    proposed, well ahead of the final $series release date.

    General Information
    -------------------

    We are still finishing up processing a few release requests, but the
    $series release requirements are now frozen. If new library releases are
    needed to fix release-critical bugs in $series, you must request a
    Requirements Freeze Exception (RFE) from the requirements team before we
    can do a new release to avoid having something released in $series that
    is not actually usable. This is done by posting to the openstack-discuss
    mailing list with a subject line similar to:

            [$PROJECT][requirements] RFE requested for $PROJECT_LIB

    Include justification/reasoning for why a RFE is needed for this lib.
    If/when the requirements team OKs the post-freeze update, we can then
    process a new release.

    A soft String freeze is now in effect, in order to let the I18N team do the
    translation work in good conditions. In Horizon and the various dashboard
    plugins, you should stop accepting changes that modify user-visible
    strings. Exceptions should be discussed on the mailing-list. By
    $rc-final-date this will become a hard string freeze, with no changes
    in user-visible strings allowed.

    Actions
    -------

    stable/$series branches should be created soon for all not-already-branched
    libraries. You should expect 2-3 changes to be proposed for each: a
    .gitreview update, a reno update (skipped for projects not using reno),
    and a tox.ini constraints URL update. Please review those in priority
    so that the branch can be functional ASAP.

    The Prelude section of reno release notes is rendered as the top level
    overview for the release. Any important overall messaging for $series
    changes should be added there to make sure the consumers of your release
    notes see them.

    Finally, if you haven't proposed $series cycle-highlights yet, you are
    already late to the party. Please see $email for details.

    Upcoming Deadlines & Dates
    --------------------------

    RC1 deadline: $rc1-deadline (R-3 week)
    Final RC deadline: $final-rc-deadline (R-1 week)
    Final Train release: $release-date
    $other-upcoming-event


R-4 week
========

#. Process any remaining client library freeze exception.

#. Freeze all cycle-based library releases except for release-critical
   bugs. Independently-released libraries may still be released, but
   constraint or requirement changes will be held until after the freeze
   period.

   .. note::

      Do not release libraries without a link to a message to openstack-discuss
      requesting a requirements RFE and an approval response from that team.

#. Propose ``stable/$series`` branch creation for all client and non-client
   libraries that had not requested it at freeze time.

   - The following command may be used::

      tox -e venv -- propose-library-branches --include-clients

   - That patch will be used as a base
     to communicate with the team: if a team wants to wait for a specific patch
     to make it to the library, someone from the team can -1 the patch to have
     it held, or update that patch with a different commit SHA.

   - On the Friday, merge patches that did not get any feedback from PTL or
     release liaison. Discuss standing -1s to see if they should be granted
     an exception and wait until next week.

#. List cycle-with-intermediary deliverables that have not been refreshed in
   the last 2 months. For this, use the following command, with YYYY-MM-DD
   being the day two months ago::

     tox -e venv -- list-deliverables --unreleased-since YYYY-MM-DD
     --model cycle-with-intermediary \
     --type horizon-plugin --type other --type service

   Send a separate email targeted to teams with such old deliverables
   saying::

    Quick reminder that for deliverables following the cycle-with-intermediary
    model, the release team will use the latest $series release available on
    release week.

    The following deliverables have done a $series release, but it was not
    refreshed in the last two months:

     {{list_of_deliverables}}

    You should consider making a new one very soon, so that we don't use an
    outdated version for the final release.

#. At the end of the week, send weekly email content preparing for R-3 week::

    Development Focus
    -----------------

    The Release Candidate (RC) deadline is next Thursday, $rc1-deadline. Work
    should be focused on fixing any release-critical bugs.

    General Information
    -------------------

    All deliverables released under a cycle-with-rc model should have a first
    release candidate by the end of the week, from which a stable/$series
    branch will be cut. This branch will track the $series release.

    Once stable/$series has been created, master will will be ready to switch
    to $next-series development. While master will no longer be feature-frozen,
    please prioritize any work necessary for completing $series plans.
    Release-critical bugfixes will need to be merged in the master branch
    first, then backported to the stable/$series branch before a new release
    candidate can be proposed.

    Actions
    -------

    Early in the week, the release team will be proposing RC1 patches for all
    cycle-with-rc projects, using the latest commit from master. If your team
    is ready to go for cutting RC1, please let us know by leaving a +1 on these
    patches.

    If there are still a few more patches needed before RC1, you can -1 the
    patch and update it later in the week with the new commit hash you would
    like to use. Remember, stable/$series branches will be created with this,
    so you will want to make sure you have what you need included to avoid
    needing to backport changes from master (which will technically then be
    $next-series) to this stable branch for any additional RCs before the final
    release.

    The release team will also be proposing releases for any deliverable
    following a cycle-with-intermediary model that has not produced any $series
    release so far.

    Finally, now is a good time to finalize release highlights. Release
    highlights help shape the messaging around the release and make sure that
    your work is properly represented.

    Upcoming Deadlines & Dates
    --------------------------

    RC1 deadline: $rc1-deadline (R-3 week)
    Final RC deadline: $final-rc-deadline (R-1 week)
    Final Train release: $release-date
    $other-upcoming-event


R-3 week (RC1 deadline)
=======================

#. Process any remaining library branching exception.

#. On the Monday, generate release requests for all deliverables
   that have do not have a suitable Train candidate yet. That includes:

   - Using `release-test` as a canary test. `release-test`
     needs to have a RC1 anyway for preparing the final release.

   - cycle-with-intermediary deliverables that have not released yet, for
     which a release should be proposed from HEAD, and include stable branch
     creation. You can list those using::

       tox -e venv -- list-deliverables --unreleased \
       --model cycle-with-intermediary \
       --type horizon-plugin --type other --type service

   - cycle-with-rc deliverables that have not done a RC1 yet, for which
     a release should be proposed from HEAD, and include stable branch
     creation. You can list those using::

       tox -e venv -- list-deliverables --missing-rc --model cycle-with-rc

   - cycle-automatic deliverables, for which a final release should be
     proposed from HEAD (unless there is an existing release in the cycle
     and no change was merged since). Those should **not** include stable
     branch creation. You can list those using::

       tox -e venv -- list-deliverables --model cycle-automatic

   - Those patches will be used as a base to communicate with the team:
     if a team wants to wait for a specific patch to make it to the release,
     someone from the team can -1 the patch to have it held, or update
     that patch with a different commit SHA.

   - Between Tuesday and Thursday, merge as soon as possible the patches that
     get +1 from the PTL or the release liaison.

   - By EOD Thursday, ideally we would want a +1 from the PTL and/or
     release liaison to indicate approval. However we will consider the
     absence of -1 or otherwise negative feedback as an indicator that the
     automatically proposed patches can be approved.

   - On the Friday, merge patches that did not get any feedback from PTL or
     release liaison. Discuss standing -1s to see if they should be granted
     an exception and wait until next week.

#. At the end of the week, send weekly email content preparing for R-2 week::

    Development Focus
    -----------------

    At this point we should have release candidates (RC1 or recent intermediary
    release) for all the $series deliverables. Teams should be working on any
    release-critical bugs that would require another RC or intermediary release
    before the final release.

    Actions
    -------

    Early in the week, the release team will be proposing stable/$series branch
    creation for all deliverables that have not branched yet, using the latest
    available $series release as the branch point. If your team is ready to go
    for creating that branch, please let us know by leaving a +1 on these
    patches.

    If you would like to wait for another release before branching, you can -1
    the patch and update it later in the week with the new release you would
    like to use. By the end of the week the release team will merge those
    patches though, unless an exception is granted.

    Once stable/$series branches are created, if a release-critical bug is
    detected, you will need to fix the issue in the master branch first, then
    backport the fix to the stable/$series branch before releasing out of the
    stable/$series branch.

    After all of the cycle-with-rc projects have branched we will branch
    devstack, grenade, and the requirements repos. This will effectively open
    them up for $next-series development, though the focus should still be on
    finishing up $series until the final release.

    For projects with translations, watch for any translation patches coming
    through and merge them quickly. A new release should be produced so that
    translations are included in the final $series release.

    Finally, now is a good time to finalize release notes. In particular,
    consider adding any relevant "prelude" content. Release notes are
    targetted for the downstream consumers of your project, so it would be
    great to include any useful information for those that are going to pick
    up and use or deploy the $series version of your project.

    Upcoming Deadlines & Dates
    --------------------------

    Final RC deadline: $final-rc-deadline (R-1 week)
    Final Train release: $release-date
    $other-upcoming-event


R-2 week
========

#. Process any standing RC1 deadline exceptions.

#. On the Monday, generate stable branches for all cycle deliverables that
   are still missing one.

   - You can list those using::

         tox -e venv -- list-deliverables --no-stable-branch

   - Those patches will be used as a base to communicate with the team:
     if a team wants to wait and make another release before the branch is
     cut, someone from the team can -1 the patch to have it held, or update
     that patch to include another release and stable branch point.

   - Between Tuesday and Thursday, merge as soon as possible the patches that
     get +1 from the PTL or the release liaison.

   - On the Friday, merge patches that did not get any feedback from PTL or
     release liaison. Discuss standing -1s to see if they should be granted
     an exception and wait until next week.

#. After all the projects enabled in devstack by default have been branched,
   we can engage with the QA, I18n and Requirements PTLs to finalize the
   stable branch setup:

   - Remind the QA PTL to create a branch in the devstack repository.
     Devstack doesn't push a tag at RC1 it is just branched off of HEAD.

   - After devstack is branched, remind the QA PTL to create a branch in the
     grenade repository. As with devstack, it will branch from HEAD instead
     of a tag.

   - Remind the QA PTL to update the default branch for devstack in the new
     stable branch. For example, https://review.opendev.org/#/c/493208/

   - Remind the QA PTL to update the grenade settings in devstack-gate for the
     new branch. For example, https://review.opendev.org/362438.

     .. note::

        As soon as grenade is updated for the new branch (see the RC1
        instructions that follow), projects without stable branches may
        start seeing issues with their grenade jobs because without the
        stable branch the branch selection will cause the jobs to run
        master->master instead of previous->master. At the end of Ocata
        this caused trouble for the Ironic team, for example.

   - Remind the I18n PTL to update the translation tools for the new stable
     series.

   - After all cycle-with-rc projects have their branches created, remind the
     requirements PTL to propose an update to the deliverable file to create
     the ``stable/$series`` branch for ``openstack/requirements``. Then
     announce that the requirements freeze is lifted from master.

     .. note::

         We wait until after the other projects have branched to
         create the branch for requirements because tests for the stable
         branches of those projects will fall back to using the master
         branch of requirements until the same stable branch is created,
         but if the branch for the requirements repo exists early the
         changes happening in master on the other projects will not use it
         and we can have divergence between the requirements being tested
         and being declared as correct.

  - Remind the QA PTL to create new branch specific jobs for our two
    branchless projects, devstack-gate and tempest, in the tempest repo.
    Configure tempest to run them on all changes, voting. Configure tempest
    to run them as periodic bitrot jobs as well. All this can be done in one
    tempest patch, for example, see https://review.opendev.org/521888.
    Configure devstack-gate to run the new jobs in check pipeline only,
    non-voting, for example see https://review.opendev.org/545144.

  - Remind the QA PTL to add the new branch to the list of branches in the
    periodic-stable job templates in openstack-zuul-jobs. For example, see
    https://review.opendev.org/545268/.

#. Ensure that all projects that are publishing release notes have the
   notes link included in their deliverable file. See
   tools/add_release_note_links.sh.

#. Let cycle-with-rc projects iterate on RCs as needed. The final release
   candidate for each project needs to be prepared at least one week before
   the final release date.

   .. note::

      Try to avoid creating more than 3 release candidates so we are not
      creating candidates that consumers are then trained to ignore. Each
      release candidate should be kept for at least 1 day, so if there is a
      proposal to create RCx but clearly a reason to create another one,
      delay RCX to include the additional patches. Teams that know they will
      need additional release candidates can submit the requests and mark
      them WIP until actually ready, so the release team knows that more
      candidates are coming.

#. At the end of the week, send weekly email content preparing for R-1 week::

    Development Focus
    -----------------

    We are on the final mile of the $series development cycle!

    Remember that the $series final release will include the latest release
    candidate (for cycle-with-rc deliverables) or the latest intermediary
    release (for cycle-with-intermediary deliverables) available.

    $final-rc-deadline is the deadline for final $series release candidates
    as well as any last cycle-with-intermediary deliverables. We will then
    enter a quiet period until we tag the final release on $release-date.
    Teams should be prioritizing fixing release-critical bugs, before that
    deadline.

    Otherwise it's time to start planning the $next-series development cycle,
    including discussing Forum and PTG sessions content, in preparation of
    $other-upcoming-event.

    Actions
    -------

    Watch for any translation patches coming through on the stable/$series
    branch and merge them quickly. If you discover a release-critical issue,
    please make sure to fix it on the master branch first, then backport the
    bugfix to the stable/$series branch before triggering a new release.

    Please drop by #openstack-release with any questions or concerns about
    the upcoming release !

    Upcoming Deadlines & Dates
    --------------------------

    Final Train release: $release-date
    $other-upcoming-event


R-1 week (Final RC deadline)
============================

#. Process any remaining stable branching exception.

#. Notify the documentation team that it should be safe to apply
   their process to create the new release series landing pages for
   docs.openstack.org. Their process works better if they wait until
   most of the projects have their stable branches created, but they
   can do the work before the final release date to avoid having to
   synchronize with the release team on that day.

#. Test the release process using the ``openstack/release-test``
   repository to ensure our machinery is functional.

#. On the day before the deadline for final release candidates,
   propose last-minute RCs where needed:

   - Check the list of unreleased changes for cycle-with-rc projects, by
     running the following command in the releases repo working directory::

     $ ./tools/list_rc_updates.sh

   - Propose patches creating a new RC for those that have unreleased
     bugfixes or updated translations

   - Patches that get a +1 from PTL or release liaison should be approved.
     A -1 will mean that the PTL prefers to wait for a post-release stable
     update. Patches that get no feedback by the deadline should be abandoned.

#. At the end of the week, send weekly email content preparing for R-0 week::

    Development Focus
    -----------------

    We will be releasing the coordinated OpenStack $series release next week,
    on $release-date. Thanks to everyone involved in the $series cycle!

    We are now in pre-release freeze, so no new deliverable will be created
    until final release, unless a release-critical regression is spotted.

    Otherwise, teams attending the PTG in $ptg-location should start to plan
    what they will be discussing there, by creating and filling team etherpads.
    You can access the list of PTG etherpads at:

    http://ptg.openstack.org/etherpads.html

    General Information
    -------------------

    On release day, the release team will produce final versions of
    deliverables following the cycle-with-rc release model, by re-tagging
    the commit used for the last RC.

    A patch doing just that will be proposed. PTLs and release liaisons should
    watch for that final release patch from the release team. While not
    required, we would appreciate having an ack from each team before we
    approve it on the 16th, so that their approval is included in the metadata
    that goes onto the signed tag.

    Upcoming Deadlines & Dates
    --------------------------

    Final Train release: $release-date
    $other-upcoming-event

#. After the email is sent, use ``propose-final-releases`` to tag the
   existing most recent release candidates as the final release for
   projects using the cycle-with-rc model.


R+0 week (Final Release)
========================

#. We are in pre-release freeze. Only release-critical regressions, or
   legal compliance issues, or bugs making it otherwise impossible to install
   and use the software on release day, should be considered by the release
   management team for a pre-release freeze exception. If approved,
   release freeze exceptions should trigger the production of a new RC (or
   cycle-with-intermediary release) and (if needed) a regeneration of the
   final release patch.

#. On release day, approve the final release patch created earlier.

   .. note::

      This needs to happen several hours before the press release
      from the foundation (to give us time to handle failures) but not
      too far in advance (to avoid releasing the day before the press
      release).

#. Once the final patch is proceesed, run the ``missing-releases`` script
   to check for missing tarballs on the release page before the announcement::

      tox -e venv -- missing-releases --series $SERIES

   If there are any missing deliverables, fix them.

#. Mark series as released on releases.o.o, by updating doc/source/index.rst
   and doc/source/$series/index.rst.
   See https://review.opendev.org/#/c/381006 for an example.

   .. note::

      This item can be staged as a patch on top of the final release patch.

#. Update the default series name in
   ``openstack/releases/openstack_releases/defaults.py`` to use the
   new series name.

   .. note::

      This item can be staged as a patch on top of the previous patch.
      Only workflow when previous step *fully* ready

#. Send release announcement email to
   ``openstack-announce@lists.openstack.org``, based on
   ``templates/final.txt``. Coordinate the timing of the email with
   the press release from the Foundation staff.

#. Send an email to the openstack-discuss list to point to the official
   release announcement from the previous step, and declare
   ``openstack/releases`` unfrozen for releases on the new series.

