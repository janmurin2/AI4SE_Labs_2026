# Software Requirements Specification

*Generated 2026-10-20 by the requirements-refinement agentic network from `corpus` (20 source documents, 752 extracted candidate requirements, 3 cluster/write/review iteration(s)).*

Models: extraction `gpt-5-mini`, clustering `gpt-6-luna`, writing `gpt-5.4-nano`, review `gpt-5.6-luna`.

## Contents
1. Priority scale
2. Glossary
3. Requirements
4. Traceability matrix
5. Discarded requirements (blacklist)
6. Quality assurance log
7. Source documents

## 1. Priority scale

Priorities follow the MoSCoW method:

| Priority | Meaning |
|---|---|
| **Must** | Essential for the system to be acceptable: core operations, legal/regulatory obligations (e.g. accessibility), security, or something stakeholders explicitly agreed is mandatory. |
| **Should** | Important and expected by stakeholders, but the system is still usable without it in a first release, or a workaround exists. |
| **Could** | Desirable improvement or convenience; implemented if time and budget allow. |
| **Won't** | Acknowledged and kept for traceability, but explicitly deferred to a later release. |

## 2. Glossary

The requirements use the following terms consistently. Terms in the last column are avoided.

| Term | Definition | Avoided synonyms |
|---|---|---|
| Item | A cataloged or uncataloged library material or copy tracked by the system. | volume (when meaning a copy or Item) |
| Item location field | The technical item-record field identifying an Item's assigned Library or other destination; this term refers to a data field, not an organizational unit. | location (as a synonym for Library or branch) |
| Library | A participating organizational library or branch within the consortium. | location (when referring to an organizational unit) |
| Library Automation System | The enterprise-level system providing library data structures and services, including such functions as acquisitions and cataloging. | ILS (as the preferred term) |
| Patron | A person with a library account. | customer |
| Report | A generated presentation of queried or aggregated system data. | output (when meaning a report) |
| Role-based access control | Authorization based on roles, security groups, and their assigned permissions. | user rights (as a standalone term) |
| Transaction | A recorded circulation or financial event, such as a checkout, hold, payment, or fine. | activity (when referring to a recorded event) |
| Transfer | A change that moves an Item from one Library or other designated destination to another. | move (as a feature name) |
| Uncataloged material | Library material tracked or circulated without an individual catalog record. | non-cat, non-cataloged |
| User | A person authenticated to use staff or administrative system functions. | Patron (when referring to staff or administrators) |
| Volume record | A bibliographic grouping record that may have associated Item records; it is distinct from an Item. | volume (when meaning an Item or copy) |

## 3. Requirements

| Priority | Count |
|---|---|
| Must | 118 |
| Should | 110 |
| Could | 9 |
| Won't | 0 |
| **Total** | **237** |

### 3.1 Cataloging

#### REQ-001: Batch Item Status Changes

- **Type:** functional
- **Priority:** Must — Batch status conversion is an essential cataloging/administrative utility explicitly agreed by stakeholders to efficiently update many Items in a single operation.
- **Sources:** `conversations/conv_pines021_item_purging.eml`
- **Derived from candidates:** C-102

The system shall provide a bulk operation that changes the status of many selected Items at once, such as changing 100 Items from one status (e.g., "missing") to another status (e.g., "discard/weed"). The system shall apply the status change to the set of selected Items in a single operation rather than requiring individual updates per Item. This requirement is needed by cataloging staff to efficiently maintain Item status during administrative workflows where large numbers of Items must be updated consistently. It also supports the efficient management of Item records at scale within the system boundary for approved administrative utilities and catalog maintenance functions.

#### REQ-002: Batch Transfer Location Updates

- **Type:** functional
- **Priority:** Must — Batch capability to update the Item location field for selected Items is an explicitly agreed core operation for completing Transfers.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-058, C-248, C-560, C-749

The system shall perform batch updates to the Item location field for Item records when executing a Transfer. It shall support selecting one or more Item records and changing their Item location field to a new destination Library or other designated destination. The system shall provide an administrative capability to change records for Items to move them to a new location destination in bulk. This requirement is needed by cataloging and administrative staff to efficiently complete Transfers without updating Items individually.

#### REQ-003: Delete Orphan Bibliographic Records

- **Type:** functional
- **Priority:** Must — The agreed requirement for an orphan-record deletion utility is essential to meet the core catalog cleanup need and make the system acceptable to stakeholders.
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-107, C-223, C-327, C-477, C-571

The system shall provide a utility to identify and delete bibliographic records that have no item records attached. The system shall generate periodic reports of bibliographic records with no item records attached and shall generate report listings of bibliographic records with no volumes attached. The system shall include a canned report for bibliographic records with no volumes attached, and shall provide a quick method to find and delete bibliographic records that have no attached item records. These capabilities support cataloging staff in cleaning up orphaned bibliographic records more efficiently by enabling both identification for review and deletion of records that have no associated Item records.

#### REQ-004: Event-Based Transfer Reversion Rules

- **Type:** functional
- **Priority:** Must — Event-based reversion behavior is core to maintaining correct Transfer outcomes and is explicitly required by agreed sources.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-063, C-064, C-065

The system shall support event-based reversion rules for Transfers that automatically revert an Item when item status changes to "returned". The system shall also support event-based rules for other item status changes, including automatically reverting an Item if its status changes to "sold" at the book sale. The system shall further support configurable event-based rules related to checkouts at the destination so that checkout can be used as a condition to keep or to revert Items. These capabilities are needed by stakeholders who manage Transfer outcomes to ensure Items are correctly reverted based on real-time status and checkout events at the destination.

#### REQ-005: Item Transfer History Tracking

- **Type:** functional
- **Priority:** Must — Transfer history at the Item level is an explicitly agreed requirement needed for transparency and operational auditing of Transfers.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-071

The system shall track and present transfer history for an Item, including the number of times the Item has been transferred (for example, “transferred 5 times in the past year”). This transfer history shall be available to staff for reviewing how an Item has changed destination over time. The capability is required because stakeholders need transparency into transfer activity at the Item level to support operational review and auditing of Transfers. 

#### REQ-006: Last-Copy Identification Report

- **Type:** functional
- **Priority:** Must — Last-copy identification is essential for cataloging and administrative maintenance workflows because the Report is explicitly treated as critical and requires accurate per-scope flagging of Items.
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-103, C-104, C-105, C-220, C-256, C-568, C-492

The system shall generate a last-copy Report that, for each Item, determines whether it is the only copy within a specified scope and flags the Item as a last copy when true. The Report shall support both a per-Library view identifying items that are the only copy within a specified Library and a system-level view identifying items that are the only copy within the entire Library system or consortium. The Report shall enable cataloging workflows by singling out the library system’s last copies to assist catalogers who need to edit external records. This capability is needed by cataloging stakeholders to identify when an Item has become the sole remaining copy within the relevant scope for subsequent catalog maintenance actions.

#### REQ-007: Manual Selection of Transfer Results

- **Type:** functional
- **Priority:** Must — Selection of specific Transfer candidates from query results is an essential operation for controlled, targeted transfers and is agreed by multiple sources.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-057, C-069, C-247, C-559

The system shall allow users to manually select individual titles from query results when performing a Transfer. The system shall also allow users to select a subset of query results so that only selected candidates are transferred. This selection capability shall support targeted transfers or actions by enabling users to include only the titles that they choose from the results set. This requirement is needed by cataloging and administrative users performing item transfers who must control which titles are included in a given Transfer.

#### REQ-008: Printable Transfer Pull Lists

- **Type:** functional
- **Priority:** Must — A Transfer pull list is essential to complete the item movement workflow and is explicitly agreed for the system.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`, `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-059, C-249

The system shall generate printable pull lists of items to be moved as part of a Transfer. The system shall provide mechanisms to move items by updating the Item location field to a new destination and by generating the corresponding pull lists. This requirement is needed by staff responsible for Transfer fulfillment because it supports retrieving the correct Items for movement and producing a print-ready list for use in operations.

#### REQ-009: Printable Transit Label Generation

- **Type:** functional
- **Priority:** Must — Without printable, barcode-based transit labels, staff cannot reliably identify items during Transfer logistics.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-060

The system shall generate printable transit labels, including barcodes, for items being transferred. Labels shall be produced for each item involved in a Transfer to support physical handling during transit. This capability is required by staff performing Transfers who need an unambiguous, scannable identifier for items moving between Libraries or other designated destinations. This requirement clarifies an administrative utility within the Library Automation System boundary for Transfer operations rather than day-to-day cataloging work.

#### REQ-010: Purge Candidate Identification Utility

- **Type:** functional
- **Priority:** Must — The agreed utility and reports for identifying Item records to purge using configurable status, time, and activity criteria are required to enable purge candidate selection.
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-095, C-096, C-097, C-098, C-099, C-254, C-566

The system shall provide a utility and reports to identify Item records to purge based on customizable criteria. The system shall support purging criteria based on Item status, including missing, discard/weed, and damaged. The system shall support purging criteria based on time-in-status (age), including being in a status for X months or X years, and shall support criteria based on activity using last circulated X days, months, or years ago. The system shall allow Library staff to configure numeric threshold values (e.g., X months/years and X days) used by these purging criteria so that the utility and reports can consistently select matching Item records. This requirement is needed by Library staff to review and validate which Item records will be purged before downstream purge actions are performed.

#### REQ-011: Read-Only Purge Candidate Reports

- **Type:** constraint
- **Priority:** Must — Reading purge candidates in a non-destructive, read-only Report is essential to safe catalog maintenance and prevents unintended deletions from the listing view.
- **Sources:** `conversations/conv_pines021_item_purging.eml`
- **Derived from candidates:** C-108

The system shall present purge candidate listings as read-only reports, with no immediate destructive action available from the report view. The listings shall be generated as a Report that identifies candidates for purging while preventing any destructive operation initiated directly from that view. This constraint ensures staff can review purge candidates safely prior to any approved destructive processing performed through other system functions. It is needed by staff performing catalog maintenance workflows who require a non-destructive review mechanism and by administrators who require clear separation between review and action.

#### REQ-012: Temporary Event Item Transfers

- **Type:** functional
- **Priority:** Must — This functionality is agreed and is core to enabling event-driven temporary routing with automatic restoration after the event.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-075

The system shall support transferring items to a temporary destination for a specific event or program and reverting those items to their prior destinations after the event. This capability shall apply to items within the system’s item-record data and shall treat the event or program as the driver for the temporary transfer and the subsequent reversion. The rationale is to allow participating libraries to support event-specific item routing while ensuring that collections return to their normal organization without manual reprocessing after the event, benefiting cataloging staff and event program administrators.

#### REQ-013: Transfer Candidate Querying

- **Type:** functional
- **Priority:** Must — Without candidate material querying, staff cannot identify which Items are eligible for Transfer, making the Transfer workflow incomplete.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-054, C-245, C-556

The system shall provide query capability to locate candidate materials for Transfer. The system shall support identifying candidate materials for Transfer using selection criteria such as collection section and last circulation date (for example, all Items in a specified section that have not circulated within a defined time period). The capability is provided to enable staff utilities that support administrative Transfer workflows by finding the set of candidate Items eligible for Transfer. This requirement is supported by an agreed query-for-candidate capability and is complemented by proposed criteria to narrow candidates for transfer.

#### REQ-014: Transfer change confirmation preview

- **Type:** functional
- **Priority:** Must — An agreed confirmation step is required to ensure Users review the Transfer scope before changes are executed.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-067

The system shall display a preview summary showing the count of affected Items and the source and destination Libraries before performing Transfer changes. The system shall require an authenticated User to confirm the preview before the system applies any Transfer changes. The confirmation requirement shall prevent the system from executing the Transfer changes based solely on a user’s initial request. This requirement is needed by staff and administrative Users to reduce the risk of unintended Transfers by reviewing the scope (source/destination and number of Items) prior to commitment.

#### REQ-015: Undo Transfer Operation

- **Type:** functional
- **Priority:** Must — Undoing mistaken transfers is an essential safeguard for correct cataloging maintenance operations and is explicitly agreed as a requirement.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-068

The system shall provide an undo function to reverse a Transfer operation when it is performed in error. This undo capability shall allow staff users to correct an incorrect transfer initiated via the transfer workflow without requiring manual re-entry of the original destination. The requirement is needed to reduce operational mistakes and recover quickly from user errors, as highlighted by the concern that an operator may click the wrong button. It applies to Transfer of an Item between a source Library and a designated destination as defined by the system’s Transfer concept.

#### REQ-016: Automatic Transfer Reversion

- **Type:** functional
- **Priority:** Should — Automatic, configurable reversion of transferred items is important operationally and reduces manual handling, but it can be mitigated by manual reversion for an initial release.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-061, C-062, C-250, C-561, C-750

The system shall include an auto-revert mechanism implemented as a scheduled task that checks transferred items and reverts them based on configured criteria. The system shall support automatic reversion of transferred items after a configurable number of days (revert after X days). The system shall be able to revert items back to their original location after the configured period, such as when a mobile library returns to base. An administrative function shall be available to revert items back to their original location. Stakeholders need this capability to ensure transferred items return automatically and administratively to their prior item location field destinations when the configured transfer period ends.

#### REQ-017: Batch Item Transfer Utility

- **Type:** functional
- **Priority:** Should — Stakeholders agreed the batch transfer utility is important for routine inter-Library movement, but the provided sources do not establish it as mandatory for system acceptability in the first release.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-053, C-244, C-555

The system shall provide a utility to perform a Transfer of batches of Items between Libraries. The system shall also support transferring batches of Items to other designated destination types, such as mobile library and outreach collections. This utility is needed by cataloging staff because batches of Items frequently must be relocated between organizational Libraries and special units. These operations enable administrative and operational handling of Item routing without changing bibliographic structures as part of this requirement.

#### REQ-018: Catalog Cleanup Performance

- **Type:** non-functional
- **Priority:** Should — Improving catalog cleanup throughput is important for cataloging productivity, but the statement does not specify measurable response or throughput targets, so it is not mandatory for initial acceptability.
- **Sources:** `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-577

The system shall provide cleanup tools and operations to reduce the time required to process orphaned records and other catalog cleanup cases. The system shall support performing cleanup using automated or assisted operations rather than requiring long manual processing by staff. This requirement is needed by cataloging stakeholders to improve staff efficiency when maintaining catalog data consistency. It addresses current pain points where cleaning up orphaned records “takes forever,” ensuring that cleanup operations complete in a timely manner without excessive manual effort.

#### REQ-019: Combined Purge Criteria

- **Type:** functional
- **Priority:** Should — Combining criteria is important for accurate purge targeting, but it is not explicitly agreed as mandatory for initial system acceptability.
- **Sources:** `conversations/conv_pines021_item_purging.eml`
- **Derived from candidates:** C-100

The system shall allow users to combine multiple purging criteria to identify purge candidates using logical operators such as AND and OR. Users shall be able to specify more than one criterion as part of a single purge-candidate identification request. This capability is needed by cataloging staff to flexibly target which Items qualify for purging based on multiple conditions. It supports administrative purge workflows that require compound selection logic rather than single-criterion filtering.

#### REQ-020: Delete Volume Records with Items

- **Type:** functional
- **Priority:** Should — Stakeholders agreed on the need for a quick deletion utility for Volume records and associated Item records, but the scope includes bulk and no-items cases that were only proposed rather than agreed.
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-106, C-257, C-570

The system shall provide a quick method to delete Volume record entries together with their associated Item records, including support for deleting Volume record entries that have no Item records attached. The method shall support bulk deletion of such Volume record entries and their associated Item records. This utility is needed by cataloging staff for efficient item-maintenance and cleanup workflows. Clarification for the system boundary: this requirement is limited to explicitly approved administrative utilities for maintenance and purge-like operations, not day-to-day ILS cataloging.

#### REQ-021: Item Status Conversion Report

- **Type:** functional
- **Priority:** Should — It is an agreed, high-value staff utility for batch item maintenance, but the system can remain usable without it via manual status updates in early releases.
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-101, C-255, C-323, C-374, C-567

The system shall provide a Report that assists staff in converting Items from one status to another in batch. The Report shall support batch conversion of item statuses by allowing a staff-configured set of Items to be converted from a source status to a destination status. The system shall enable batch use cases such as changing 100 Items from “missing” to “discard/weed.” This capability is needed by cataloging staff to perform efficient administrative item maintenance when multiple Items require status updates, subject to the project’s system boundary for approved administrative utilities.

#### REQ-022: Quick Distribution for Uncataloged Materials

- **Type:** functional
- **Priority:** Should — It is important for efficient branch operations and fast processing of incoming uncataloged material, but it is not evidenced as mandatory for initial system acceptability.
- **Sources:** `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-241, C-551, C-552

The system shall support quick distribution workflows for uncataloged material so incoming materials can be processed fast. The system shall provide low-effort processing operations that minimize per-item branch labor, including for large shipments, to enable efficient handling with limited staff time. This capability applies to uncataloged material tracked or circulated without an individual catalog record. The requirement is needed by library staff to reduce time spent per item and to accelerate processing of uncataloged shipments at branches, particularly during high-volume arrivals.

#### REQ-023: Saved Reusable Transfer Queries

- **Type:** functional
- **Priority:** Should — Recurring transfer workflows depend on reusing saved query definitions frequently, but the core transfer capability can still function without scheduled re-running in an initial release.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-055, C-077, C-246, C-557, C-558

The system shall allow users to save queries for repeated use so staff can re-run commonly used item transfer queries. The system shall support reusing saved queries on a regular basis, such as monthly, to support recurring transfer workflows (for example, moving all Items in a specified genre that have not circulated in a defined time period). The system shall provide this capability within the item transfer utility. This enables administrative cataloging/transfer workflow efficiency for staff who perform the same transfer operations repeatedly.

#### REQ-024: Transfer Delay User Notifications

- **Type:** functional
- **Priority:** Should — It is an agreed requirement for timely transfer issue awareness, but it is not described as a mandatory regulatory or security constraint.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-070

The system shall send alerts to designated authenticated Users if an Item Transfer is delayed or encounters issues. Alerts shall be based on transfer status conditions indicating delay or problems, as requested by users who want to be notified when such issues occur. This capability supports operational awareness and timely resolution of transfer problems for staff who manage transfers.

#### REQ-025: Transfer Destination Types

- **Type:** functional
- **Priority:** Should — This is an agreed, practical feature for creating Transfers to common delivery destinations, but it is not strictly required for initial system usability if an alternative workflow exists.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-076

The system shall allow a staff User to select a destination location type when creating a Transfer. The selectable destination location types shall include mobile library units, outreach programs, and just-in-time warehouses. This selection is used to define the intended destination category for the Transfer being created. Stakeholders need this capability to support transfers to operational delivery models such as mobile units and outreach programs, and to a just-in-time warehouse workflow.

#### REQ-026: Uncataloged Inventory Tracking

- **Type:** functional
- **Priority:** Should — It is important for practical cataloging workflows involving shipments without catalog records, but it is not explicitly indicated as a legal/security critical requirement in the provided candidates.
- **Sources:** `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-240, C-550

The system shall provide the ability to control inventory of uncataloged material, such as paperback books and children’s board books. The system shall allow tracking uncataloged material as inventory even when individual catalog records (volume record) are not present. This capability supports handling large shipments that arrive without individual catalog records, enabling staff to track and manage those items as Item inventory under the system’s boundary for administrative utilities rather than replacing day-to-day ILS cataloging.

#### REQ-027: WorldCat Last-Copy Workflow Support

- **Type:** functional
- **Priority:** Should — It is important for catalogers’ last-copy operations via WorldCat editing, but its implementation details and system boundary relative to core cataloging responsibilities should be confirmed.
- **Sources:** `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-569

The system shall support integration or workflow aids with WorldCat so catalogers can edit external bibliographic records for last-copy items. This support is intended to complement the system’s last-copy workflow by enabling catalogers to perform the required external record updates. The last-copy report and WorldCat integration are considered critical to enable this catalog maintenance work. This requirement is needed by catalogers and cataloging operations that rely on timely and accurate external bibliographic updates.

#### REQ-028: Scheduled Purging Utility

- **Type:** functional
- **Priority:** Could — Automation of purging on a configurable schedule is useful but was only explicitly proposed and questioned in the source, with no agreed contractual requirement.
- **Sources:** `conversations/conv_pines021_item_purging.eml`
- **Derived from candidates:** C-112

The system shall be able to schedule the purging utility to run automatically on a configurable schedule (for example, annually). This capability shall allow administrators to trigger the purging process without manual execution by running it at the configured recurrence interval. The functionality is needed by stakeholders responsible for catalog maintenance to support periodic cleanup and reduce operational effort. It is also needed to ensure purging can be performed consistently according to agreed maintenance cycles.

### 3.2 Documentation

#### REQ-029: Functional-Focused Initial Specification

- **Type:** constraint
- **Priority:** Must — The agreed meeting decision explicitly mandates an initial focus on functional requirements with UI details deferred.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-625

The system shall establish initial specifications that emphasize functional requirements. Detailed user interface specifications shall be deferred to later iterative specification rather than included in the initial specification set. This approach ensures the stakeholders first align on what the system must do before committing to UI details, supporting efficient progression of requirements work.

#### REQ-030: Online Hierarchical Help System

- **Type:** documentation
- **Priority:** Must — Accessible online help that works with screen readers and covers all system functions is essential for acceptable system usability and compliance.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-185, C-532, C-608, C-647, C-690, C-691

The system shall provide an online help system in HTML that is hierarchical and cross-linked, and that describes and illustrates all system functions. The system shall ensure the online help system is accessible and works with screen readers. The system shall include help that is integrated with the reports interface and supports navigation through the help content. The online help system shall also provide searchable content to support users in finding system functions. This requirement is needed by patrons, system administrators, and technical stakeholders to ensure complete, discoverable, and accessible documentation for using all system functions.

#### REQ-031: Outreach Use-Case Test Scenarios

- **Type:** documentation
- **Priority:** Must — Stakeholders agreed that outreach test scenarios are required to validate the inactive-patrons Report outputs.
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Derived from candidates:** C-171

The system shall rely on project stakeholders to provide test scenarios for outreach use cases in order to validate the inactive-patrons Report. These test scenarios shall specifically cover the conditions required to confirm that the inactive-patrons Report is generated correctly for outreach-related validation. This documentation is needed so stakeholders can perform consistent verification of inactive-patrons reporting outcomes during outreach use case testing.

#### REQ-032: Record Data Dictionary Specifications

- **Type:** documentation
- **Priority:** Must — Complete data specifications are essential for the Management Processes to correctly maintain and access all required record types.
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-183, C-645, C-681, C-682, C-683, C-684, C-685, C-686

The system shall provide complete data specifications (data dictionary) for authority records, bibliographic records, order records, item records, hold/request records, and other records maintained or accessed by the Management Processes. These data specifications shall include the full set of record definitions necessary to support the Management Processes’ use of each record type. The system shall ensure the same level of completeness applies across all listed record categories. This requirement is needed by the Management Processes stakeholders to ensure consistent, unambiguous record structures for development and integration.

#### REQ-033: Separate missing/damaged and in-transit reports

- **Type:** documentation
- **Priority:** Must — It is agreed that the report requirements must be tracked separately in project documentation to support correct documentation and traceability.
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`
- **Derived from candidates:** C-091

The system shall ensure its project documentation records the missing/damaged report and the in-transit report as two separate requirements. This documentation distinction shall be maintained so that each report requirement is tracked independently while still being understood as related. This requirement supports stakeholders’ review and traceability of report-specific behavior for the documentation process agreed in the project conversations.

#### REQ-034: SRS Basis and Documentation Approach

- **Type:** documentation
- **Priority:** Must — These documentation commitments are essential to define and align the system requirements and to communicate them to both library and software delivery stakeholders.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-609, C-610, C-624

The system shall have its requirements specification based on the King County Library System/Galecia Group draft, adapted for PINES. The system shall be documented in an SRS that specifies optimal Reports functionality for a future Evergreen release and includes a list of requirements. The SRS shall be written for both library managers and staff and for software project managers and developers, balancing readability for non-technical readers with specificity for developers. This basis and documentation approach is needed to ensure consistent requirements traceability and to support both operational stakeholders and delivery teams.

#### REQ-035: Track Material Volume Report Requirement

- **Type:** documentation
- **Priority:** Must — Because the source is agreed and explicitly states the Material Volume Report requirement must be tracked as a key requirement, it is essential for acceptable requirements maintenance.
- **Sources:** `conversations/conv_pines014_material_volume.eml`
- **Derived from candidates:** C-019

The system shall record and track the Material Volume Report requirement as a key requirement within the project's requirements tracker. The system shall ensure this requirement is included in the tracker as an explicitly maintained key requirement. This requirement is needed by stakeholders responsible for maintaining and monitoring project requirements through the requirements tracker process.

#### REQ-036: Working Group Report Testing Gate

- **Type:** constraint
- **Priority:** Must — An agreed governance constraint is required to ensure all new Report development is reviewed by the designated testing group.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-611

The system shall filter all new Report development through the Reports Working Group, which shall act as the reports testing group. This filtering shall ensure that any new Reports produced by the system development process are reviewed by the Reports Working Group prior to acceptance. The requirement is needed by the Reports Working Group and system stakeholders to establish a consistent testing and governance gate for all new Reports.

#### REQ-037: Attached Report Specifications

- **Type:** documentation
- **Priority:** Should — Supporting the attached reporting definitions and fine-grained reports requirements is important for meeting agreed reporting expectations, but the provided sources are only proposed rather than agreed or explicitly mandatory.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-227, C-228

The system shall support the reporting definitions described in the attached report examples in Appendix A, and it shall support the fine-grained reports requirements described in the attached specification in Appendix B. These capabilities ensure the system can generate the required Report content and structure as specified by the reporting materials supplied to the project, which is needed by stakeholders responsible for reporting requirements and validation against the appendix documents.

#### REQ-038: Capacity Interface Mockups

- **Type:** documentation
- **Priority:** Should — Providing initial UI mockups is important for aligning stakeholders early, but the system can be acceptable with later refinements in a first release.
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`
- **Derived from candidates:** C-034

The system shall produce initial UI mockups for the system capacity interface. Initial mockups shall be drafted for review in support of the capacity interface documentation. This requirement exists to provide stakeholders with an early visual representation of the capacity interface to guide subsequent specification and refinement.

#### REQ-039: Interview-Based Requirements Intake

- **Type:** documentation
- **Priority:** Should — It is important for deriving correct report needs from member libraries, but it is marked as proposed with a dated deliverable rather than an explicit mandatory requirement.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-632

The system shall base its requirements on interviews with staff at member libraries conducted by working group members. Each member shall conduct at least one interview with staff at their library system to gather report needs, with the interviews due by April 15, 2009. This ensures the requirements are informed by member library report needs and that stakeholders have a shared basis for subsequent requirements work.

#### REQ-040: Iterative UI Prototype Specification

- **Type:** constraint
- **Priority:** Should — Collaborative iterative prototyping is important for aligning the interface and underlying data structures with end-user needs, but it is not strictly necessary for an initial acceptable release.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-626, C-629

The system shall specify its user interface and data structures using an iterative, prototype-oriented methodology. The system shall be developed in a highly collaborative and iterative environment that provides multiple opportunities for end-user review of prototypes. This requirement ensures that stakeholder feedback can be incorporated early and throughout development, benefiting end-users and the team responsible for user interface and data structure definition.

#### REQ-041: Major Process Descriptions

- **Type:** documentation
- **Priority:** Should — Thorough documentation of major processes is important for stakeholder understanding and review, but the system can be acceptable without it in an initial release.
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-184, C-646, C-687, C-688, C-689

The system shall include a high-level process description for bibliographic record import and export, for validation of bibliographic records against internal and external authority sources, and for standard reports. The high-level descriptions shall be thorough and cover these major processes as part of the system documentation. This requirement is needed by the system stakeholders to understand how core bibliographic workflows operate and how the system generates standard reports. It also supports developer and reviewer alignment on process behavior related to authority validation and record data exchange.

#### REQ-042: Overview Display Large-Count Investigation

- **Type:** documentation
- **Priority:** Should — An investigation and documented findings are important for implementing the overview at the required scale, but the system could be workable initially with follow-on refinement once constraints are understood.
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`
- **Derived from candidates:** C-035

The system shall investigate technical constraints and report findings for displaying a large number of Libraries (286) in the overview. This investigation shall consider how the overview handles rendering and performance implications associated with that number of Libraries. The findings shall be documented as part of the project’s documentation work. This requirement is needed to help stakeholders understand feasibility and technical limitations before implementing the overview display for the expected scale.

#### REQ-043: Patron Null Field Documentation

- **Type:** documentation
- **Priority:** Should — This documentation is important for correct report interpretation, but the system can function without it in an initial release.
- **Sources:** `conversations/conv_pines023_patron_characteristics.eml`
- **Derived from candidates:** C-144

The system shall document which Patron data fields may be inconsistently populated and specify how missing values (nulls) are represented and handled in reports. The documentation shall ensure that report consumers understand the expected null behavior for fields that may not be consistently available. This supports stakeholders who need accurate interpretation of report data when Patron characteristics are incomplete.

#### REQ-044: Architecture Review Meetings

- **Type:** documentation
- **Priority:** Could — A structured architecture review process is beneficial for coordinating architectural constraints, but it is not described as mandatory for system acceptability or compliance.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-631

The system’s requirements process shall include architecture review meetings and a technical subcommittee. The requirements process shall schedule and hold at least one technical subcommittee meeting in late June to discuss architectural constraints. The requirements process shall schedule and conduct a follow-up review meeting on July 20, 2009 to continue the discussion of architectural constraints. This requirement is needed by the project stakeholders who must coordinate and document architecture decisions through a formal review cadence.

#### REQ-045: Assumed Library Terminology Knowledge

- **Type:** assumption
- **Priority:** Could — This is a documentation scope assumption intended to streamline the SRS, but the system would remain acceptable if common terminology were defined instead.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-630

The system shall assume that readers have a general understanding of Library services and processes and therefore need not define common Library terminology within the SRS. This assumption applies to the SRS readers’ need for explanations of terminology rather than to any operational behavior of the system. The purpose of this assumption is to reduce unnecessary documentation detail while maintaining shared baseline understanding. Stakeholders who author and review the SRS need this assumption to streamline terminology coverage.

### 3.3 Operating Environment

#### REQ-046: Acquisition Date Used for Reporting

- **Type:** assumption
- **Priority:** Must — Acquisition-date-driven Reports and date-window queries depend on the database containing acquisition dates for Items, making it essential for acceptable reporting behavior.
- **Sources:** `conversations/conv_pines014_material_volume.eml`
- **Derived from candidates:** C-018

The system shall use each Item’s acquisition date stored in the database to compute acquisition-based Reports and date-window queries. This acquisition date data assumption ensures that reporting and query logic can be driven by the database field rather than external inputs. Stakeholders needing this are reporting consumers and system operators who rely on consistent acquisition-date reporting across the environment. 

#### REQ-047: Assistive Technology Accessibility Support

- **Type:** non-functional
- **Priority:** Must — Accessibility support and Section 508 compliance are explicitly required and agreed by stakeholders.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-177, C-531, C-589, C-590, C-591, C-592, C-638, C-664, C-669

The system shall be accessible with screen-reading software, screen-magnification software, and other assistive technology programs. The system shall comply with Section 508 accessibility requirements. The system shall be usable with common screen readers such as JAWS and NVDA and with screen magnification software such as ZoomText, and it shall be compatible with other assistive technology programs used by staff. The system shall provide accessibility support for the report interface and ensure HTML output is compatible with different browsers and assistive technologies such as screen readers.

#### REQ-048: Background Report Processing

- **Type:** non-functional
- **Priority:** Must — Blocking interactive operations during long-running or complex reports is explicitly identified as requiring background queuing and processing to meet stakeholder expectations.
- **Sources:** `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`
- **Derived from candidates:** C-526, C-584

The system shall provide background processing for long-running reports so they do not block interactive operations. The system shall support queuing and background processing of complex reports so they can run asynchronously without impacting interactive use. This capability is needed by system administrators to ensure report execution does not degrade interactive performance for users.

#### REQ-049: Configuration Migration Import/Export

- **Type:** functional
- **Priority:** Must — Stakeholders agreed that migration requires export/import of report templates, permission settings, and saved queries as core operating-environment functionality.
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-711, C-712, C-713

The system shall provide export and import of report templates to support migration between environments. The system shall provide export and import of permission settings to support migration between environments, including the permission settings associated with the exported configuration. The system shall provide export and import of saved queries to support migration between environments, so that saved query definitions can be moved along with templates and permissions. This capability is needed by stakeholders to enable consistent configuration transfer across environments during migration activities.

#### REQ-050: Consortium Scale Capacity

- **Type:** non-functional
- **Priority:** Must — Meeting the agreed consortium scale is essential to ensure the system can operate acceptably under expected annual circulation and item processing volumes.
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Derived from candidates:** C-172, C-633

The system shall support a library consortium with at least 286 Libraries, 17 million annual circulations, and purchasing/processing of over 900,000 Items per year. The system shall be capable of sustaining these volumes as an operating environment requirement for consortium operations. This requirement ensures the system’s scalability matches the agreed consortium workload and is needed by the consortium stakeholders and system planners to confirm overall feasibility.

#### REQ-051: Enterprise ILS Infrastructure Assumptions

- **Type:** assumption
- **Priority:** Must — Without these enterprise and integration environment assumptions, the Management Processes cannot operate or interoperate with required infrastructure and related systems.
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-187, C-188, C-189, C-190, C-191, C-627, C-649, C-650, C-651, C-652, C-653, C-694, C-695, C-696, C-697

The system shall assume that the Management Processes are part of an enterprise-level Library Automation System and can rely on that system’s infrastructure. The system shall assume that enterprise infrastructure services are available, including redundant servers, backup systems, and network connectivity. The system shall assume the Management Processes rely on the data structures and functionality of an enterprise-level Library Automation System, including Acquisitions and Cataloging modules, and that the Management Processes are consolidated at a central location to accept input and provide services to multiple locations. The system shall assume interaction with a patron interface also known as an Online Public Access Catalog (OPAC), and that the system can interface with vendor websites via published APIs and/or automated transfer of standard-format data files such as USMARC21 and EDIFACT. These assumptions are required so stakeholders can plan the operating environment and integration dependencies for the Management Processes within the enterprise Library Automation System context.

#### REQ-052: Immediate Financial Data Reflection

- **Type:** non-functional
- **Priority:** Must — Immediate reflection of recorded payments is essential to keep financial data current for reporting and reconciliation, as agreed by stakeholders.
- **Sources:** `email_financial_reports.eml`
- **Derived from candidates:** C-413

The system shall reflect updates to financial information immediately when staff record a payment, including payments made at the front desk, so the financial data is current for reporting and reconciliation. This requirement ensures that each recorded Transaction is available for downstream Report generation and reconciliation without delay, minimizing the risk of discrepancies. It is needed by library staff responsible for accurate financial reporting and reconciliation and by stakeholders who require up-to-date financial data for operational integrity.

#### REQ-053: In-Transit Data Availability Assumption

- **Type:** assumption
- **Priority:** Must — This is an agreed operating-environment assumption that must hold for in-transit tracking and any dependent functions to operate correctly.
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`
- **Derived from candidates:** C-094

The system shall assume it currently tracks Item status values such as "missing" and "long overdue" and that it maintains a transit table including arrival and departure dates. This assumption underpins any processing that relies on in-transit tracking data being available for Items during operation. It is needed so stakeholders can plan system behavior and data dependencies based on the existing system’s capabilities.

#### REQ-054: Inactive Report Background Performance

- **Type:** non-functional
- **Priority:** Must — Background execution and caching are essential to prevent interactive performance degradation and maintain acceptable report responsiveness, while scaling expectations ensure feasibility for large datasets.
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Derived from candidates:** C-165, C-166, C-170

The system shall run the inactive-patrons query as a background job to avoid degrading interactive system performance. The system shall cache report results for the inactive-patrons report to improve performance for repeated access to the same dataset. The system shall be designed to scale to large patron databases, such as on the order of 3.5 million patrons, without unacceptable performance degradation. This requirement is needed by stakeholders responsible for operational performance and by patrons who rely on responsive interactive system behavior while inactive-report processing occurs.

#### REQ-055: Management Process Scope

- **Type:** constraint
- **Priority:** Must — This is an agreed scope constraint that defines what the system will cover for management process reporting and analysis.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-614, C-628

The system shall focus on Management Processes, providing reports and analysis tools used by library managers, administrators, and staff to support planning, evaluation, and oversight. The system shall specify only those requirements that directly or indirectly relate to management activities, excluding requirements that do not have such a relationship. This constraint ensures the operating environment and functional scope remain aligned with stakeholder expectations for management-focused capabilities and clearer requirement traceability for managers and administrators.

#### REQ-056: Non-Disruptive Reporting During Open Hours

- **Type:** non-functional
- **Priority:** Must — Disrupting OPAC or the circulation client during open hours is unacceptable to stakeholders and would undermine core library operations.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-173, C-546, C-586, C-634, C-680

The system shall enable searches and reports to be processed during open hours without disrupting other system functions. The system shall separate reporting operations from production operations to avoid impacting production performance. The system shall ensure searches, reports, and report processing do not disrupt or slow down the OPAC or circulation client during open hours. The system shall queue and perform long-running searches and report generation in background processing so report generation does not slow down or disrupt the circulation client. The system shall not constrain or interfere with the OPAC and shall not slow down OPAC performance when reports run. This requirement is needed by library staff and system operators to maintain service availability for patron-facing clients while reporting is executed.

#### REQ-057: OPAC Read-Only and No Patron Functions

- **Type:** constraint
- **Priority:** Must — This is essential to establish system scope and prevent unauthorized or conflicting behavior with the OPAC and the authoritative acquisition/cataloging processes.
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-182, C-615, C-644, C-698, C-700

The system shall not include day-to-day patron-facing functions; such functions shall remain part of the Online Public Access Catalog (OPAC) module and the circulation client. The system shall interact with the patron interface (OPAC) in a read-only manner and shall not modify OPAC data. The system shall not constrain the functionality or features of the Online Public Access Catalog (OPAC) module. The system shall not manage acquisitions or cataloging functions, and it shall read and report on ILS data instead. This boundary clarifies the operating environment responsibilities needed by consortium stakeholders to ensure the OPAC and circulation client remain authoritative for patron workflows and bibliographic maintenance, while the reporting system remains non-invasive.

#### REQ-058: Patron Reporting Data Fields

- **Type:** assumption
- **Priority:** Must — The system’s patron reporting requires the specified patron table fields to be present; otherwise reporting cannot be performed correctly.
- **Sources:** `conversations/conv_pines023_patron_characteristics.eml`
- **Derived from candidates:** C-143

The system shall assume that the patron table contains the fields age (birth_date), zip code, county, home branch, patron type, and preferred language for reporting purposes. This assumption enables reporting logic to query and aggregate patron characteristics consistently. Stakeholders such as operations and reporting stakeholders need this structure to ensure generated Reports reflect the intended patron attributes.

#### REQ-059: Relational Database Backend and Schema

- **Type:** constraint
- **Priority:** Must — A fully relational, PostgreSQL-compatible design aligned to the existing normalized schema is an agreed platform constraint required for acceptance.
- **Sources:** `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-178, C-581, C-582, C-583, C-639, C-665, C-666, C-667

The system shall use a fully relational database back-end. The system shall be compatible with PostgreSQL databases, operating against the environment’s PostgreSQL 8.3. The system shall operate against the existing normalized relational database schema and shall not require denormalized reporting schemas. The system shall avoid denormalized reporting schemas that would create synchronization issues. This constraint is needed by the system administrators and technical stakeholders to ensure the new system aligns with the existing database platform and schema maintenance practices.

#### REQ-060: Secondary Disaster Recovery Deployment

- **Type:** constraint
- **Priority:** Must — Deployment to the secondary disaster recovery site is agreed as essential for resilient reporting operations.
- **Sources:** `interview_sysadmin_2009-05-10.txt`
- **Derived from candidates:** C-607

The system shall be deployable to the secondary disaster recovery site for reporting operations. The system’s reporting operations shall run successfully on the secondary disaster recovery site environment, which is specified as Solaris 10 on SPARC hardware. This constraint supports continuity of reporting in the event of a primary site failure and is required by the system administrators responsible for disaster recovery and reporting operations.

#### REQ-061: Separated Dev/Test Environments

- **Type:** constraint
- **Priority:** Must — Separate environments and configuration migration are required to safely develop and train without impacting production and to support moving reporting configuration into production.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-180, C-529, C-530, C-547, C-603, C-604, C-605, C-606, C-641, C-642, C-670, C-671, C-672

The system shall provide separate development, training, and production environments so developers and staff can test and practice running reports without affecting production data or operations. The system shall provide the ability to migrate reporting configuration from the development and training environments to the production environment. Reporting configuration migration shall support exporting and importing report templates and related configuration, including permission settings and saved queries. The system shall provide a development and training environment that is safe for staff experimentation without risking production data, and this configuration migration capability shall be available to support management processes. This requirement is needed by system administration and management stakeholders to support safe development and training and to enable controlled promotion of reporting configuration into production.

#### REQ-062: Standards-Compliant HTML Output

- **Type:** non-functional
- **Priority:** Must — These requirements are agreed and explicitly define standards compliance and accessibility-related HTML content needed for acceptable web, report, and help presentation.
- **Sources:** `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-179, C-593, C-594, C-595, C-596, C-640, C-668

The system shall generate standards-compliant, properly structured semantic HTML for web-based components, reports, and help content. The system shall ensure its HTML validates against W3C standards for all web-based interfaces and report output. For images included in the HTML output, the system shall provide alt attributes. For interactive elements, the system shall include ARIA labels where appropriate to improve accessibility.

#### REQ-063: Supported Server Operating Systems

- **Type:** constraint
- **Priority:** Must — Stakeholders agreed the system must run on Linux and Solaris, including specific Red Hat Enterprise Linux 5 and Solaris 10 SPARC environments for primary and disaster recovery.
- **Sources:** `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Derived from candidates:** C-174, C-578, C-579, C-580, C-635

The system shall operate on a server environment running Linux or Solaris. It shall be deployable and operable on Red Hat Enterprise Linux 5 for the primary server environment. It shall also be deployable and operable on Solaris 10 on SPARC hardware to support the secondary/disaster recovery site. The system shall work across both Linux and Solaris platforms so that system reporting and operations are available in either environment. This constraint is needed by the system stakeholders responsible for operations and disaster recovery to ensure the system can be deployed on their existing server platforms.

#### REQ-064: Supported Web Browsers

- **Type:** constraint
- **Priority:** Must — Stakeholders agreed the system must support Internet Explorer 6.0+ and Mozilla Firefox 2.0+ to be acceptable for web-browser access.
- **Sources:** `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Derived from candidates:** C-176, C-587, C-588, C-637

The system shall be accessible through Microsoft Internet Explorer version 6.0 and later and Mozilla Firefox version 2.0 and later when accessed via a web browser. This constraint applies to the system’s web-browser-based access, including management process access. This requirement is needed by the system administrators and management to ensure the system functions in the browsers currently in use.

#### REQ-065: Vendor Website Interface Support

- **Type:** functional
- **Priority:** Must — Interfacing with vendor websites is essential for Management Processes to integrate and exchange data with external systems.
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-699

The system shall interface with vendor websites using published APIs and/or automated transfer of standard-format data files. The supported data file formats shall include USMARC21 and EDIFACT. This capability shall enable Management Processes to connect to a variety of vendor websites through approved integration mechanisms. This requirement is needed by the technical subcommittee stakeholders to ensure interoperability with external vendors and to support automated data exchange.

#### REQ-066: Web and Windows Client Access

- **Type:** functional
- **Priority:** Must — Access through a web browser or a Windows-compatible client is agreed and is essential for stakeholders to use the system’s management functions.
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Derived from candidates:** C-175, C-636

The system shall be accessible through a web browser or a Windows-compatible client. This accessibility method applies to the system’s management processes as well. This requirement ensures stakeholders can access the system using common client options for day-to-day operations and management workflows.

#### REQ-067: Centralized Capacity Data Assumption

- **Type:** assumption
- **Priority:** Should — It is an important operating-environment assumption to support cross-branch capacity aggregation, but it is qualified by “unless analysis shows otherwise.”
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`
- **Derived from candidates:** C-036, C-033

The system shall assume that capacity-related data is centralized in the system database unless analysis shows otherwise. The system shall use the centralized database as the basis for aggregating capacity data across all Library Automation System branches by querying that database. This requirement is needed to establish a common operating assumption and data access approach for stakeholders defining capacity analysis and reporting across the consortium.

#### REQ-068: Evergreen Version and Reporting Assumptions

- **Type:** assumption
- **Priority:** Should — The assumption is important to align requirements with the PINES production baseline, but it is not inherently a core functional/security obligation for system acceptance.
- **Sources:** `evergreen_reference_2009.txt`
- **Derived from candidates:** C-548, C-549

The system shall assume the analysis and requirements apply to the Evergreen codebase version 1.4.0.4 and the PINES production usage patterns. The system shall further assume the current Evergreen reporting implementation runs queries against the production database and that no separate reporting database replica exists. This assumption ensures that requirements behavior and expected data access patterns are grounded in the production environment used by stakeholders at PINES.

#### REQ-069: In-Transit Detection Logic

- **Type:** constraint
- **Priority:** Should — It is an important detection behavior for correct operational handling, but it is derived from a questioned proposal and needs alignment with the separate topic of status and transit data availability.
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`
- **Derived from candidates:** C-092

The system shall identify in-transit Items by checking the transit table for records where the arrival date is null and the departure date is more than X days ago. The requirement is intended to be a testable detection rule that flags in-transit records based on these transit-table date fields. This enables operating-environment logic needed for downstream handling of Items that have departed but have not yet arrived, supporting operations stakeholders who require reliable in-transit identification.

#### REQ-070: Large Batch Transfer Updates

- **Type:** constraint
- **Priority:** Should — Efficient, transaction-safe batch processing is important for large-catalog Transfer operations, but the system may remain usable with less optimized batching in an initial release.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-073, C-074

The system shall process batch updates efficiently for very large catalogs by applying updates in smaller batches to avoid locking the database. The system shall perform batch updates of the item location field using transaction safety so that partial updates cannot result in inconsistent state. This requirement supports the stakeholders who need reliable Transfer processing at consortium scale and database integrity during large catalog updates.

#### REQ-071: Reporting Replica Offload

- **Type:** functional
- **Priority:** Should — It is an important agreed mechanism to achieve separation of reporting from production, though the evidence indicates the broader separation requirement exists elsewhere and this specific database/replica approach may be an implementation option.
- **Sources:** `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`
- **Derived from candidates:** C-525, C-585

The system shall run reporting workload using a separate reporting database or a read-only reporting replica to offload reporting queries from the production database. This approach ensures reporting workload does not execute against the production database. The system shall be able to use read-only reporting replicas for this purpose. This requirement is needed to support non-disruptive separation of reporting from production operations for stakeholders operating and maintaining production services.

### 3.4 Reporting

#### REQ-072: Acquisition Window Reporting

- **Type:** functional
- **Priority:** Must — Stakeholders agreed that configurable acquisition-window reporting is required to provide timely insight into recent acquisitions.
- **Sources:** `conversations/conv_pines014_material_volume.eml`
- **Derived from candidates:** C-013

The system shall allow reporting of Items acquired within configurable windows, such as the last 30, 60, or 90 days. The acquisition-window reporting shall support configuring the window so that the generated Report reflects the Items acquired in the selected period. This capability is needed by stakeholders to quantify how much Item volume has been added over recent time periods for acquisition review and planning.

#### REQ-073: Activity Metrics Reporting

- **Type:** functional
- **Priority:** Must — Activity Metrics reporting is explicitly agreed and provides core circulation-hold usage statistics needed for acceptable reporting functionality.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`
- **Derived from candidates:** C-211, C-432

The system shall produce Reports showing traffic and volume of use. The Reports shall include statistics for check-outs, check-ins, holds placed, and holds filled. This functionality enables staff and other stakeholders to understand system usage and circulation activity at a summary level for reporting and decision-making.

#### REQ-074: Administrator Error Feedback Reporting

- **Type:** functional
- **Priority:** Must — Clear error reporting and administrator-level query diagnostics are essential to acceptable report troubleshooting and operation.
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-186, C-648, C-692, C-693

The system shall provide thorough high-level error reporting and feedback when reports fail. The system shall allow Local and Global System Administrators to view low-level, query-specific error feedback from the front-end interface. The query-specific error feedback shall include table, field, and error type where possible. This requirement is needed by Local and Global System Administrators to diagnose report failures using both summary (high-level) and detailed (query-specific) information.

#### REQ-075: Aged In-Transit Reporting

- **Type:** functional
- **Priority:** Must — This capability is agreed and covers the core reporting behavior, including threshold, branch/system scope, merged transit directions, and periodic generation needed by reporting stakeholders.
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-083, C-086, C-084, C-219, C-252, C-564, C-085, C-093, C-253, C-565

The system shall generate a list of items that have been in-transit for more than X days, where X is configurable. The in-transit threshold X shall default to 7 days unless reconfigured. The system shall produce the in-transit report per Library Automation System branch and for the entire system, and it shall merge transit-to and transit-from records into a single in-transit report. The system shall generate periodic reports of items that have been in-transit for more than X days.

#### REQ-076: Automated Shelf Space Report Generation

- **Type:** functional
- **Priority:** Must — Automating Shelf Space Report generation eliminates the agreed core pain point of tedious manual spreadsheet creation, making the system acceptable to stakeholders.
- **Sources:** `conversations/conv_pines016_shelf_space.eml`
- **Derived from candidates:** C-049

The system shall automate generation of the Report so staff do not need to pull reports manually and create spreadsheets. This requirement addresses the current workflow where staff manually pull reports and build spreadsheets, which is described as tedious. The automated generation capability is needed by staff to reduce manual effort and improve reporting efficiency for Shelf Space reporting.

#### REQ-077: Branch Capacity Filtering

- **Type:** functional
- **Priority:** Must — Filtering, sorting, and grouping are core capabilities required to make branch capacity reporting usable for stakeholder analysis.
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`
- **Derived from candidates:** C-023, C-024, C-025, C-026, C-030

The system shall allow users to sort the branch list by chosen fields or metrics. The system shall allow users to filter branches by region, by library type, and by current load. The system shall allow users to group branches by system or region for the overview display. This requirement enables users to refine and organize branch capacity reporting so relevant stakeholders can analyze capacity conditions across the consortium.

#### REQ-078: Branch Capacity Overview

- **Type:** functional
- **Priority:** Must — The requirement is agreed and defines the core branch capacity overview interface used for reporting at both summary and branch-detail levels.
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`, `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-020, C-021, C-037, C-237

The system shall provide an interface that shows the capacity of all Library branches in the system at once. The system shall provide a high-level summary view that displays all branches and key capacity metrics together. The system shall display key capacity metrics for each branch in both the overview and branch-detail views. This capability is needed by reporting stakeholders to quickly assess branch-level capacity and compare metrics across branches. 

#### REQ-079: Cancel Scheduled or Running Reports

- **Type:** functional
- **Priority:** Must — Cancelling scheduled and running report execution with prompt stoppage is essential operational functionality agreed by the technical subcommittee.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-385, C-514, C-707, C-708, C-733

The system shall allow users or administrators to cancel a scheduled report or a running report. When a report is in progress, the system shall check for cancellation signals during report processing so running jobs can be stopped promptly. This capability covers report jobs that are already scheduled to run or are currently running, and ensures cancellation can take effect during processing rather than only between processing phases. The requirement is needed by stakeholders who operate reporting workflows and require the ability to halt report execution when it is no longer desired.

#### REQ-080: Capacity Data CSV Export

- **Type:** functional
- **Priority:** Must — Exporting capacity data to CSV is an agreed core reporting operation needed for stakeholders to use and reuse capacity outputs outside the system.
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`
- **Derived from candidates:** C-027

The system shall provide an export function that allows capacity data to be exported to CSV. This requirement covers only the export capability and the CSV format for capacity data, while relying on other requirements for capacity reporting content and structure. It is needed by reporting stakeholders who require a portable, machine-readable extract of capacity data for analysis, sharing, and downstream processing.

#### REQ-081: Check-In Type Counts

- **Type:** functional
- **Priority:** Must — Counting check-in types individually and cumulatively is a core reporting need explicitly required by the proposed requirement.
- **Sources:** `early_draft_srs_galecia.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-270, C-717

The system shall count all types of check-in individually and cumulatively, including book-drop, and provide counts by terminal and by user or self-service. The system shall treat each check-in type (including book-drop and terminal and user/self-service channels) as separate counts while also maintaining cumulative totals across all check-in types. This enables reporting stakeholders to understand check-in patterns and overall volumes needed for operational and management oversight.

#### REQ-082: Collection Usage Analysis Reports

- **Type:** functional
- **Priority:** Must — Without collection usage Report and analysis tools, the system cannot deliver the core reporting capability agreed for this requirement area.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-616

The system shall provide Report and analysis tools to analyze the library collection and its use by patrons. These tools shall support generating reports based on queried or aggregated system data to support collection-usage analysis. This requirement enables stakeholders to understand how the library collection is being used by patrons and to make informed reporting decisions based on those analyses.

#### REQ-083: Deletion Audit Report Interface

- **Type:** functional
- **Priority:** Must — This capability is required to support auditing and staff troubleshooting by querying and reporting on deletions across defined dimensions and time periods.
- **Sources:** `conversations/conv_pines022_deletions.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-121, C-122, C-123, C-124, C-125, C-126, C-128, C-130, C-258, C-572, C-751

The system shall provide a Report interface that can query a deletion audit table and present deletion data to Users. The system shall produce Reports showing deletions per Library and per system, and it shall provide aggregation of deletion data by date range, by User, and by record type. The system shall support total deletions for configurable reporting periods such as month, quarter, and year, and it shall break down deletions by record type (e.g., Item vs Patron vs other). The system shall produce Reports listing the top Users who delete the most records to help identify anomalies, and it shall provide audit data sufficient for auditors to demonstrate that deletions occurred in accordance with retention schedules and policies. The system shall allow staff to search and inspect deletion audit entries to troubleshoot why a specific record disappeared.

#### REQ-084: Demographic Statistics Reports

- **Type:** functional
- **Priority:** Must — This capability is explicitly agreed and required to generate demographic statistics from archived transactions while preserving individual privacy to support program planning.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-233, C-437, C-662, C-721

The system shall produce aggregated demographic statistics derived from archived transactions, including transactions by geographical region and transactions by age ranges. The system shall provide useful aggregated demographic statistics for demographic analysis reports that support program planning. The system shall preserve individual privacy while generating the aggregated demographic statistics. Stakeholders needing program planning and reporting analytics require these demographic views to understand transaction patterns across regions and age ranges without exposing individual data.

#### REQ-085: Electronic Activity for Last Activity

- **Type:** functional
- **Priority:** Must — This requirement defines which logged behaviors count toward “last activity,” which is essential for correct inactive patron reporting.
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Derived from candidates:** C-149, C-150, C-151, C-152, C-167, C-168

The system shall treat OPAC/patron account logins as electronic activity when determining each patron’s last activity. The system shall treat online hold placements as electronic activity when determining each patron’s last activity. The system shall treat online renewals as electronic activity when determining each patron’s last activity. The system shall treat access to digital collections as electronic activity when such access is integrated and logged, and shall compute last activity by combining activity records from the relevant circulation, OPAC logins, holds, renewals, and digital access logs sources into a unified last-activity calculation per patron. The system shall determine each patron’s most recent activity by querying the transaction and related activity tables, comparing the last activity date to X days for filtering inactive patrons. This is needed by reporting stakeholders to reliably identify inactive patrons using consistent definitions of electronic activity.

#### REQ-086: Email Report Delivery

- **Type:** functional
- **Priority:** Must — Email delivery of reports is explicitly required to send generated reports to recipients, and existing sources indicate it is a core expectation rather than a deferred enhancement.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-371, C-512, C-730

The system shall allow entering email addresses for report delivery and support an address book of regularly used addresses. The system shall support delivering scheduled or on-demand reports via email. Email delivery shall enable sending one or more generated reports to one or more recipients.

#### REQ-087: Executive Report Templates

- **Type:** functional
- **Priority:** Must — Executive and board reporting templates and the Executive Reports Interface are required to meet mandated Georgia Annual Report statistics and to support routine executive reporting consumption.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Derived from candidates:** C-210, C-431, C-612, C-655, C-663

The system shall provide pre-defined Board and Executive reports for consumption by library boards and external consumers. These pre-defined board reports shall include basic statistics required by the Georgia Annual Report and similar external reporting needs. The system shall provide an Executive Reports Interface and include a compiled list of reports needed for that interface. The system shall provide pre-defined board and executive report templates to support routine executive reporting.

#### REQ-088: Financial Transaction Record Association

- **Type:** functional
- **Priority:** Must — Accurate association and joinability of financial data across patron and item records is essential for generating financial reports.
- **Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-278, C-399, C-414, C-543

The system shall attach fines, charges, waivers, and ecommerce transactions to patron records and item records in the database. The system shall support joining the financial data attached to patron records and item records when generating financial reports. The system shall make reportable records for action_circulation, action_hold, and money (fines/payments) available for reporting and linking to patrons and items. This requirement is needed by staff and reporting stakeholders to ensure financial report generation can accurately relate financial transactions to the relevant patron and item.

#### REQ-089: Historical Volume Reporting

- **Type:** functional
- **Priority:** Must — Historical comparisons based on point-in-time volume counts are an agreed core reporting capability for this category.
- **Sources:** `conversations/conv_pines014_material_volume.eml`
- **Derived from candidates:** C-011, C-012

The system shall provide date filters to produce volume counts as of any specified point in time. The system shall provide reports that show volume changes over time to support historical comparisons. This enables staff and other stakeholders to analyze how volumes evolve between dates and to retrieve point-in-time counts for comparison.

#### REQ-090: Hold Placement Method Reporting

- **Type:** functional
- **Priority:** Must — Capturing the placement method for every hold request is essential to produce the intended holds reporting breakdown by staff desk, public computer, and remote placement.
- **Sources:** `early_draft_srs_galecia.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-272, C-719

The system shall count all hold requests and record how each hold was placed. The recorded placement method options shall be at a staff desk, at a public computer inside the Library, or remotely. The system shall include the method of placement when generating holds count reports so that holds can be reported by placement method. This requirement enables stakeholders to analyze and survey how patrons place holds, supporting reporting needs identified in the early drafts and survey results.

#### REQ-091: Inactive Patron Outreach Fields

- **Type:** functional
- **Priority:** Must — These fields and exclusions are required to generate an effective and compliant inactive-patrons report for outreach.
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Derived from candidates:** C-157, C-158, C-159, C-160, C-161, C-162

The system shall include each Patron's current mailing address in the inactive-patrons report for outreach purposes. The system shall identify or flag inactive patrons who have outstanding fines so they can be handled separately. The system shall allow excluding patrons marked with a “do not disturb” flag, excluding VIP patrons, excluding staff member accounts, and excluding patrons who have opted out of communications from the inactive-patrons report. These capabilities are needed by library staff to produce accurate outreach lists that respect patron preferences and internal handling rules.

#### REQ-092: Inactive Report CSV Export

- **Type:** functional
- **Priority:** Must — Exporting the inactive-patrons report as CSV in an upload-ready format is explicitly agreed and required for downstream outreach/marketing use.
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Derived from candidates:** C-163, C-164

The system shall provide the inactive-patrons report in an exportable CSV format. The system shall produce exported report files in a format suitable for upload into external outreach/marketing systems, including the ability to be uploaded to an outreach system.

#### REQ-093: Include Null and Blank Values

- **Type:** functional
- **Priority:** Must — Including null and blank fields in report results is essential for report correctness and prevents misleading omissions.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-386, C-538, C-709, C-734

The system shall include all nulls and blank fields in report results for any report, rather than omitting them. The system shall not implicitly filter out null or blank fields due to filtering or display settings. When null and blank fields are requested, the system shall include them in the results explicitly. This requirement is needed by stakeholders who rely on complete and accurate reporting outputs for downstream analysis and validation.

#### REQ-094: Include Patron Null Values

- **Type:** functional
- **Priority:** Must — This is essential to prevent patron records with missing field values from being dropped and to ensure report results accurately reflect the underlying data.
- **Sources:** `conversations/conv_pines023_patron_characteristics.eml`
- **Derived from candidates:** C-137

The system shall include patron records with null (missing) values in report results rather than silently excluding them, and display nulls in the relevant fields. This behavior ensures that patron characteristic reporting remains accurate by preserving records where expected patron data is not present. Stakeholders who need complete patron reporting, including staff preparing analyses and users validating report outputs, require this to avoid incomplete results caused by missing data.

#### REQ-095: Item and Bibliographic Field Reporting

- **Type:** functional
- **Priority:** Must — Core reporting requires filtering by bibliographic content and presenting bibliographic_record and Item fields in a row-based Report for staff users.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-320, C-393, C-539, C-540

The system shall generate a Report listing Items whose bibliographic_record contains a specified string in a specified field. The system shall pull MARC record fields and present selected fields on a single row of Report data. The system shall make bibliographic_record fields available to reporting, including id, fingerprint, edition, ISBN, publisher_name, publication_date, and physical_description. The system shall make item fields available to reporting, including id, barcode, copy_number, item location field, status, call_number, purchase_date, shelving_location, and reserve_id, where item location field is the technical item-record field identifying an Item’s assigned Library or other destination. This capability is needed by staff users to support flexible reporting and analysis across bibliographic_record and Item metadata.

#### REQ-096: Item Value Reporting

- **Type:** functional
- **Priority:** Must — This provides the core “value of items” reporting functionality required by agreed reporting expectations and depends on using the purchase price field for value aggregation.
- **Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-276, C-395, C-396, C-397, C-398, C-322, C-497

The system shall generate a report of the value of items based on data in item records for the entire collection or for a selected portion of the collection. The system shall use the item record purchase price field as the source of item value and be able to query and aggregate that field to support the report. The system shall allow value reports to be filtered by item status and by collection attributes such as format (e.g., DVDs in a children’s collection) to enable staff to obtain value for relevant subsets. This capability is needed by library staff to produce value reporting across an entire collection or targeted segments for decision-making and financial awareness.

#### REQ-097: Library Shelf Space Comparison View

- **Type:** functional
- **Priority:** Must — This is essential reporting functionality specifically required to compare Libraries’ Shelf Space metrics side-by-side and against the system average.
- **Sources:** `conversations/conv_pines016_shelf_space.eml`
- **Derived from candidates:** C-047, C-050

The system shall provide a comparison view that displays multiple Library Shelf Space Report breakdowns side-by-side so that outliers can be identified. The system shall display, for each Library, how its Shelf Space metrics compare to the system average. This capability supports reporting stakeholders such as branch managers who need to understand their local situation and benchmark it against the system-wide average.

#### REQ-098: Material Quantity Categories

- **Type:** functional
- **Priority:** Must — Agreed requirements establish that customizable categories and category-based reporting of material quantities and holds are essential for acceptable reporting.
- **Sources:** `conversations/conv_pines014_material_volume.eml`
- **Derived from candidates:** C-009, C-014, C-015

The system shall allow Libraries to define and use customizable categories for breaking down material quantity counts. The system shall group and report material quantity counts by reporting categories such as fiction/non-fiction and by format. The system shall show holds counts broken down per reporting category. This is needed by Libraries to configure reporting groupings and by reporting stakeholders who need consistent breakdowns for both material quantity and holds.

#### REQ-099: Material Quantity Library Scope

- **Type:** functional
- **Priority:** Must — Correct Library scoping is essential for acceptable Material Quantity report results and for stakeholder confidence in the reporting outputs.
- **Sources:** `conversations/conv_pines014_material_volume.eml`
- **Derived from candidates:** C-010

The system shall restrict item counts to Items whose Item location field equals the selected Library, so counts include only Items assigned to that Library. The system shall apply this restriction when calculating Material Quantity report results for the selected Library. This requirement ensures consistent, testable scoping for reporting so stakeholders can trust that reported quantities correspond to the intended organizational Library or branch.

#### REQ-100: Material Volume Report

- **Type:** functional
- **Priority:** Must — It is agreed core functionality for on-demand material volume visibility by Library, including the consolidated report and required subcounts/period support.
- **Sources:** `conversations/conv_pines014_material_volume.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-001, C-002, C-003, C-004, C-005, C-006, C-007, C-008, C-016, C-017, C-235, C-236, C-574

The system shall provide the ability to report on the volume of material in a given Library at any point in time. For a selected Library, the system shall report the count of new acquisitions (items recently added), the count of items on the shelf (checked in), and the count of items out in circulation (checked out), and shall report an aggregate total across these statuses. The system shall also report the number of holds for the selected Library and provide category breakdown counts for adult fiction and board books. The system shall provide a single consolidated Material Volume Report so users do not have to pull data manually from multiple screens, and it shall support generating reports for standard reporting periods used by libraries (for example, monthly and quarterly reports). This capability is needed by library stakeholders to produce consistent material volume reporting without manual cross-screen compilation.

#### REQ-101: Metadata Last-Edit Date Reporting

- **Type:** functional
- **Priority:** Must — Displaying an accurate metadata last-edit date on item reports is essential for meeting stakeholders’ expectations of correct report content.
- **Sources:** `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-576

The system shall display a last-edit date on item reports that reflects the most recent metadata edit. The last-edit date displayed in the report shall exclude any circulation activity so that the value is not affected by circulation events. This requirement is needed by stakeholders who require visibility into when an Item’s metadata was last changed for accurate reporting and review.

#### REQ-102: Missing and Damaged Item Reporting

- **Type:** functional
- **Priority:** Must — Stakeholders agreed the system must generate missing and damaged Reports per Library with auditing counts and include Items in 'missing' or 'lost' status.
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Derived from candidates:** C-079, C-080, C-089, C-251, C-315, C-562, C-659

The system shall provide missing and damaged item Reports broken down per Library. The system shall include counts of missing and damaged Items in the Report to support auditing. The system shall include Items with status values 'missing' or 'lost' (or equivalent) in the missing/damaged Report. This capability is needed by stakeholders to generate the requested missing/damaged item visibility per Library and to show how many Items went missing or were damaged for auditing purposes.

#### REQ-103: Multi-format Report Export

- **Type:** functional
- **Priority:** Must — This is an agreed requirement ensuring core report export deliverables in Excel, HTML, and CSV for stakeholder use.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-370, C-461, C-701, C-702, C-703, C-729

The system shall export report results in Excel, HTML, and CSV formats. It shall support exporting report results in CSV format, HTML for web display, and Excel format suitable for pivot tables. The exported report output formats shall include CSV, HTML, and Excel to accommodate different stakeholder reporting workflows. This requirement is needed by business users and staff to obtain report results in the formats required for analysis and web viewing.

#### REQ-104: Patron Age Range Calculation

- **Type:** functional
- **Priority:** Must — Accurate, configurable age-range computation from birth_date is essential for patron age reporting in Reports.
- **Sources:** `conversations/conv_pines023_patron_characteristics.eml`
- **Derived from candidates:** C-138, C-139

The system shall compute a patron's age range at query time by calculating age from the birth_date field. The system shall allow age range (age bracket) boundaries to be configured per report, such that reports can use boundaries like 0-5, 6-10, 11-15 or alternatives such as 0-6, 7-12. This requirement is needed by stakeholders who generate demographic and patron characteristic Reports and need consistent, report-specific age bracket definitions.

#### REQ-105: Patron Characteristic Grouping

- **Type:** functional
- **Priority:** Must — Stakeholders agreed that Patron characteristic-based limiting and grouping is required to support the core reporting use cases.
- **Sources:** `conversations/conv_pines023_patron_characteristics.eml`, `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-133, C-259, C-260, C-261, C-262, C-263, C-264

The system shall allow queries and reports to be limited or grouped by patron age range, zip code, county of residence, home branch, patron type, and preferred language. The system shall support using these patron characteristics as criteria for both queries and aggregated Report generation. This requirement is needed by stakeholders who require Patron demographic analysis and targeted Reporting based on different patron attributes.

#### REQ-106: Patron Data Availability for Reports

- **Type:** functional
- **Priority:** Must — Patron fields are mandatory source data for creating and running patron-related reports.
- **Sources:** `evergreen_reference_2009.txt`
- **Derived from candidates:** C-541

The system shall make patron fields available to reporting, including id, barcode, family_lib, usr_grp, email, address, birth_date, and create_date. For reporting purposes, address shall be composed of address lines, city, state, and zip (postal code). The system shall include family_lib as the home library and usr_grp as the patron type. The system shall include email as the em field and shall provide create_date and birth_date for patron records. This requirement is needed by stakeholders who develop or configure reports that rely on patron identifiers and key patron attributes for querying and aggregation.

#### REQ-107: Patron Payment Ledger Reconciliation

- **Type:** functional
- **Priority:** Must — Accurate and auditable reconciliation between patron payments and the specific charges they apply to is essential for finance staff to perform financial reconciliation and traceability.
- **Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`
- **Derived from candidates:** C-286, C-409, C-410

The system shall maintain a ledger of patron payments and record which charges each payment was applied to in order to facilitate reconciliation. The system shall maintain this as an audit ledger of patron payments so finance staff can trace every payment back to the specific charge it was applied to. This capability ensures finance-related reconciliation workflows are supported by providing auditable payment-to-charge associations needed by finance staff and stakeholders responsible for financial reporting integrity.

#### REQ-108: Patron Report Filtering

- **Type:** functional
- **Priority:** Must — Filtering patron reports with configurable LIMIT and combined AND/OR logic is essential to generate the correct patron subset for reporting needs.
- **Sources:** `conversations/conv_pines023_patron_characteristics.eml`
- **Derived from candidates:** C-134, C-136

The system shall support LIMIT (filter) operations on patron reports so users can restrict the returned patron set by one or more characteristics. The system shall allow multiple filters to be combined using AND and OR logic when building patron reports. This capability is required by stakeholders who need to produce targeted patron reporting results for focused analysis and decision-making.

#### REQ-109: Patron Report Grouping

- **Type:** functional
- **Priority:** Must — Agreed functionality for GROUP BY patron reporting is required to produce attribute-grouped counts demanded by stakeholders.
- **Sources:** `conversations/conv_pines023_patron_characteristics.eml`
- **Derived from candidates:** C-135, C-140, C-141

The system shall support GROUP BY (aggregate) operations on patron reports so users can compute and display aggregated metrics grouped by patron characteristics. The system shall enable grouping of circulation (checkout) counts by patron characteristics such as age range. The system shall also enable grouping of patron counts by patron characteristics such as home branch. This capability is needed by reporting stakeholders who require demographic- and attribute-based breakdowns within patron reports.

#### REQ-110: Payment Reporting by Method

- **Type:** functional
- **Priority:** Must — Finance stakeholders require payment reporting broken down by both time period and payment method types for acceptable financial reporting.
- **Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`
- **Derived from candidates:** C-285, C-405, C-406

The system shall provide reports of payments made per time period and broken down by payment method types. Payment method types shall include cash, credit card, check, and similar methods, and shall be reported using payment methods such as staff desk, self-check station, and OPAC. The reporting shall aggregate payment totals according to the selected time period and the chosen payment method breakdown so stakeholders can analyze payment composition and channels. This requirement is needed by finance and operations stakeholders to understand payment intake patterns for reporting and reconciliation purposes.

#### REQ-111: Query Criteria Picklist Selection

- **Type:** functional
- **Priority:** Must — Selecting query-criteria values from picklists is essential to acceptable report query building functionality for staff.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`
- **Derived from candidates:** C-206, C-417

The system shall allow staff to select values for query criteria from a picklist of possible values when building queries. This capability shall support staff in choosing among predefined criteria values rather than entering them manually. The requirement is needed by reporting stakeholders to ensure efficient and consistent query construction for report generation.

#### REQ-112: Real-Time Reporting Support

- **Type:** functional
- **Priority:** Must — Stakeholders agreed that some reporting needs to be real-time (e.g., what is overdue today) and surveys indicate it is needed for busy-period monitoring.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-387, C-516, C-704, C-736

The system shall provide real-time reporting capabilities by generating reports based on up-to-the-minute transactional data. The system shall support reporting on live changes as required, including reports that reflect current overdue items as of today. The system shall provide real-time or near-real-time reporting capability adequate for monitoring busy periods. This requirement ensures staff can monitor critical operational conditions using the most current transactional data, particularly for overdue items and high-demand times.

#### REQ-113: Report Criteria Display

- **Type:** functional
- **Priority:** Must — Users must be able to view the report’s applied criteria (including date range and report name) to understand and validate generated report results.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-225, C-389, C-390, C-438, C-521

The system shall display the query selections (criteria) alongside the query results so users can see what criteria were used to generate the report. When configuring reports, the system shall present selection criteria that are clearly defined to users. The system shall include the date selection criteria and report name at the top or bottom of report results to indicate the selected date range and report name. This capability is needed by users to interpret report results and to verify the criteria used to produce them.

#### REQ-114: Report Query Builder Interface

- **Type:** functional
- **Priority:** Must — Staff require an interface to design and execute queries across all core record types, and custom/local reporting is essential for stated library use cases.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-204, C-415, C-459, C-533, C-534, C-745

The system shall provide a user-friendly interface for designing queries against all record types, including bibliographic, item, patron, transaction, and financial. The system shall also provide a web-based report writer interface that supports drag-and-drop field selection. The system shall support creation, storage, and execution of custom/local reports used by libraries for collection development, program tracking, and staff productivity. This capability is needed by Library staff to build and run the queries and reports required for day-to-day library operations and reporting needs.

#### REQ-115: Report Query Field Selection

- **Type:** functional
- **Priority:** Must — Selecting query fields is core functionality for creating usable Reports via the query interface.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-205, C-368, C-416, C-464

The system shall allow staff to select which fields to query through the query interface when defining a Report. The system shall support staff checking off or selecting specific data/fields to include in the report. The system shall expose all relevant database fields for selection in report definitions rather than limiting selection to a subset. This capability is needed by staff to configure reports based on the specific fields they require for their reporting needs.

#### REQ-116: Report Template Creation

- **Type:** functional
- **Priority:** Must — Template creation and management are essential to enable staff reporting using templates for all Library units.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-195, C-421, C-613, C-724, C-527

The system shall allow administrators to create report templates that are available to staff. The system shall provide a report template management capability for creating, storing, and versioning templates. The system shall also support determining and creating report templates needed for all Library units within the consortium. Created report templates shall be capable of being run as-is or modified before running. This capability is needed by administrators and reporting stakeholders to ensure staff can generate required reports using managed, reusable templates.

#### REQ-117: Report Template Integrity

- **Type:** non-functional
- **Priority:** Must — Accurate report results following template changes are essential to acceptable reporting outcomes.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-197

The system shall ensure that changes to templates do not compromise the accuracy of results. This requirement covers integrity of results produced when report templates are changed, so that stakeholders can trust reporting outputs after template updates. It is needed by reporting stakeholders who rely on accurate results for decision-making and by developers who must maintain correctness through template evolution.

#### REQ-118: Report Template Run and Edit

- **Type:** functional
- **Priority:** Must — It is required to enable controlled template modification while preserving report result integrity and consistent criteria for acceptable reporting.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`
- **Derived from candidates:** C-196, C-198, C-199, C-375, C-422, C-423, C-424, C-425

The system shall allow report templates to be run as-is or be modified for individual needs, and it shall allow staff to edit canned reports for display purposes. Administrators shall be able to limit which filters and display fields in a template can be altered by staff so the system can certify dependable output. The system shall prevent staff from altering templates to display deleted items or other administrator-restricted data, and it shall prevent or warn about modifications that would compromise the intended results of a report template. The system shall centrally manage report templates to ensure consistent criteria when staff run standard reports. This is needed by administrators and staff to safely reuse templates while maintaining consistent, dependable report results.

#### REQ-119: Shelf Space Comparison Report

- **Type:** functional
- **Priority:** Must — It defines the core contents of the Shelf Space Report required to perform the stated percentage comparisons for planning decisions.
- **Sources:** `conversations/conv_pines016_shelf_space.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Derived from candidates:** C-038, C-039, C-040, C-041, C-044, C-045, C-238, C-573, C-661

The system shall provide a Report, the Shelf Space Report, that for each genre and format enables comparison of the percentage of total circulations, the percentage of the collection (by item count), and the percentage of total shelf space. The system shall calculate the percentage of total circulations for each genre and format by summing checkouts per genre and format. The system shall calculate the percentage of the collection for each genre and format by counting items per genre and per format. The system shall calculate the percentage of total shelf space occupied by each genre and format. This requirement is needed by cataloging and reporting stakeholders to support shelf space utilization and collection/space planning comparisons.

#### REQ-120: Shelf Space Estimation Per Genre

- **Type:** functional
- **Priority:** Must — This estimation behavior is required to generate shelf-space estimates from available data because shelf space is not directly tracked in the database.
- **Sources:** `conversations/conv_pines016_shelf_space.eml`
- **Derived from candidates:** C-046

The system shall estimate shelf space per genre and format using existing data. For each genre and format, the system shall use item dimension data where available to produce the shelf space estimate. When direct shelf-space measurements are not available, and item dimension data is not available for the relevant items, the system shall fall back to item count as a proxy for shelf space. The system shall provide these estimates to support shelf-space-related reporting needs for stakeholders who require capacity and distribution visibility without having direct shelf-space measurements.

#### REQ-121: Shelf Space Report Organizational Scope

- **Type:** functional
- **Priority:** Must — Accurate shelf space reporting requires both per-Library and system-level scope as a core, agreed reporting deliverable.
- **Sources:** `conversations/conv_pines016_shelf_space.eml`, `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-042, C-043, C-239

The system shall produce the Shelf Space Report for individual libraries (per-branch) as well as for the whole system using an aggregated system-level view. The system shall support aggregation/grouping of report results at different organizational levels equivalent to applying GROUP BY at the appropriate level for the per-library or system-wide breakdown. This capability enables stakeholders to analyze shelf space at both the local Library level and the consolidated consortium level from the same reporting scope.

#### REQ-122: Sort In-Transit Reports by Due Date

- **Type:** functional
- **Priority:** Must — Front-line staff depend on due-date ordering of the in-transit report to prioritize urgent in-transit items, and the requirement is agreed.
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`
- **Derived from candidates:** C-087

The system shall allow the in-transit report to be sorted by due date so front-line staff can address the oldest items first. This sorting capability shall enable staff to prioritize in-transit items based on their due dates when reviewing the in-transit report. The rationale is to support operational workflow for front-line staff who need to chase the oldest items first.

#### REQ-123: Transaction Audit Query

- **Type:** functional
- **Priority:** Must — Audit reporting for Transactions scoped by date/time and workstation or staff member is essential to support investigation and verification needs.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-394

The system shall allow running a Report of Transactions that occurred on a specified date and time, filtered by either a specified workstation or a specified staff member. The report criteria shall support selecting the occurrence date and time and selecting the relevant workstation or staff member to scope the returned Transactions. This requirement supports audit and investigations by enabling staff to retrieve the exact subset of recorded circulation or financial events for a targeted time and actor.

#### REQ-124: Transaction Report Scopes

- **Type:** functional
- **Priority:** Must — Correct transaction report scope and granularity are essential so stakeholders can generate the required circulation and hold reports at patron, Library, system, and county levels.
- **Sources:** `early_draft_srs_galecia.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-273, C-274, C-720, C-741

The system shall generate transactions reports for holds placed, holds filled, and check-outs at the following aggregation scopes: per patron, per Library, per selected group of Libraries, per system, and per county. The system shall display, within patron-scoped transaction reports, the number of check-outs and the number of placed holds. The system shall support transaction report dimensions that match these scopes while reflecting the relevant transaction types (holds placed, holds filled, and check-outs). The rationale is to enable reporting stakeholders to analyze circulation and hold activity by individual patrons and by varying organizational and geographic groupings, supporting both operational review and survey-driven reporting needs.

#### REQ-125: Validated Report Output

- **Type:** non-functional
- **Priority:** Must — Validated, correct report output with de-duplicated tabular exports is essential for stakeholders to rely on reporting results.
- **Sources:** `early_draft_srs_galecia.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-384, C-737

The system shall provide tested and proven Report output, ensuring validated output formats and correctness. The system shall ensure data exported to Excel and other tabular formats does not contain unintended duplicate rows. This requirement is needed so stakeholders can trust that generated reports use correct formats and produce accurate, reliable tabular exports.

#### REQ-126: Waived Fine Reporting

- **Type:** functional
- **Priority:** Must — Reporting on fines waived by time period and branch/library is an agreed financial reporting requirement necessary for acceptable system behavior.
- **Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`
- **Derived from candidates:** C-284, C-404

The system shall provide reports showing fines waived per configurable time period and per branch. The report scope shall be at the Library level as defined by the participating branch or library within the consortium. This capability allows stakeholders to monitor waived fines consistently across branches over time, supporting financial reporting needs identified in the early drafts and confirmed by stakeholders.

#### REQ-127: Activity Cross-Tabulation

- **Type:** functional
- **Priority:** Should — Cross-tabulation across these dimensions is important for reporting analysis but is not explicitly indicated as mandatory by the sources beyond agreement.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`
- **Derived from candidates:** C-212, C-433

The system shall allow cross-tabulation of activity statistics per terminal, branch, library system, hour, patron age range, patron type, and patron location. The system shall support generating cross-tabulated report metrics using these same dimensions: terminal, branch, system, hour, age range, patron type, and patron location. This capability enables stakeholders to analyze activity variations across multiple operational and patron characteristics for reporting and decision-making.

#### REQ-128: Administrative Candidate Material Queries

- **Type:** functional
- **Priority:** Should — It is an important administrative reporting capability for selection/weeding workflows, but it is not explicitly described as mandatory for initial system acceptability.
- **Sources:** `survey_results_2009.txt`
- **Derived from candidates:** C-747

The system shall provide an administrative query function that identifies candidate materials for purposes such as selection or weeding. The query function shall be able to return candidate material results that can be used to support administrative decision-making. This capability is needed by administrative staff to efficiently locate and assess candidate materials during curation and weeding workflows.

#### REQ-129: Administrative Query Result Selection

- **Type:** functional
- **Priority:** Should — Administrators need a way to target specific items from query results for subsequent actions, but the system can still be usable without manual selection as long as an alternative selection workflow exists.
- **Sources:** `survey_results_2009.txt`
- **Derived from candidates:** C-748

The system shall allow administrators to manually select items from query results for further actions. The system shall support manual selection of items originating from query results so administrators can choose a subset for subsequent processing. This capability is needed to support administrative workflows that require human selection rather than fully automated query output. It is especially relevant to administrators performing targeted actions based on the contents of a generated query result set.

#### REQ-130: Batch Report Execution

- **Type:** functional
- **Priority:** Should — Batching multiple canned reports into one document is important for efficient reporting workflows, but the system can remain usable without it in an initial release.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-364, C-511

The system shall allow users to select multiple canned reports to run at the same time. The system shall allow users to check off multiple canned reports from a list for simultaneous execution. The system shall display the results of concurrently executed selected reports within a single document. This enables stakeholders to efficiently produce and review multiple Report outputs together without requiring separate executions.

#### REQ-131: Bibliographic Record Activity Reports

- **Type:** functional
- **Priority:** Should — These bib record activity reporting metrics are important for staff visibility into bibliographic record creation and edit activity, but the sources indicate some candidates were not available yet.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-324, C-325, C-326, C-476, C-498, C-499

The system shall generate a Bib Records Count report and a Bib Records Edited Count report. The system shall generate a report of Bib Records added by user by library with counts using the Bib Records Added by user by library Count metric. The system shall include a canned report for Bib Records Count. The system shall include a Bib Records Edited Count report, noting it was indicated as not available. The system shall provide a report of Bib Records added by user by library with counts, noting it was indicated as not available.

#### REQ-132: Branch Capacity and Collection Distribution Analysis

- **Type:** functional
- **Priority:** Should — It is an agreed reporting requirement, but it is not directly restated with measurable acceptance metrics in the provided candidates beyond the existence of the reports and analysis tools.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-617

The system shall provide reports and analysis tools to analyze branch capacity and determine the optimal distribution of the collection. The analysis shall support evaluating how capacity constraints relate to recommended collection distribution across Libraries. This capability is needed by stakeholders to make data-driven decisions about branch planning and collection allocation based on branch capacity and collection distribution findings.

#### REQ-133: Branch Capacity Drilldown

- **Type:** functional
- **Priority:** Should — Drilldown from summary to branch-level capacity detail is an important reporting usability function but can be worked around by alternate ways of viewing capacity details.
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`
- **Derived from candidates:** C-022

The system shall allow users to drill down from the high-level summary into detailed capacity information for an individual branch. This capability provides the interface to view per-branch capacity detail starting from the aggregated branch capacity summary, as agreed in PINES-015. The requirement is needed by stakeholders who want to inspect capacity at branch level without losing context from the summary view.

#### REQ-134: Branch Capacity Trend Display

- **Type:** functional
- **Priority:** Should — Trend direction (growing vs. shrinking) is an important reporting insight but can be worked around with separate historical capacity views in early releases.
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`
- **Derived from candidates:** C-028

The system shall display trend data indicating whether a Library branch is growing or shrinking over time. This capability is required for users who need to understand branch capacity direction across time within the capacity interface.

#### REQ-135: Branch-Grouped Reports

- **Type:** functional
- **Priority:** Should — Branch grouping is an agreed reporting capability, but it can be useful without being strictly required for an initial release.
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`
- **Derived from candidates:** C-088

The system shall allow reports to be grouped by Library branch. This grouping shall support generating report results based on queried or aggregated system data such that the grouping dimension corresponds to Library branch. This capability is needed by stakeholders who require branch-level organization of reporting outputs for analysis and comparison.

#### REQ-136: Canned Missing Status Report

- **Type:** functional
- **Priority:** Should — A canned report for Items with Missing Status is important for routine data review and reduces effort, but it is still usable if deferred while core reporting capabilities are delivered first.
- **Sources:** `evergreen_reference_2009.txt`
- **Derived from candidates:** C-475

The system shall include a canned report listing Items with Missing Status. This canned Report shall present the set of Items where Missing Status applies, as part of the system’s standard reporting offerings. This requirement supports staff and administrators who need a repeatable way to identify and review Items with Missing Status without building a custom query each time.

#### REQ-137: Canned Report Display Options Editing

- **Type:** functional
- **Priority:** Should — Enabling edits to canned report display options is important for maintainability and usability, but the system may still be acceptable using non-editable options in an initial release.
- **Sources:** `evergreen_reference_2009.txt`
- **Derived from candidates:** C-522

The system shall allow editing of canned report display options. This requirement is needed because stakeholders require staff to modify how a canned Report is displayed without being limited to a fixed set of presentation settings.

#### REQ-138: Canned Report Templates

- **Type:** functional
- **Priority:** Should — Providing shipped canned report templates and permission-controlled extensibility is important for practical reporting adoption, though it can be partially worked around without adding new templates in an initial release.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-362, C-376

The system shall include a set of pre-written canned report templates delivered with the product. The system shall allow adding more canned reports based on role-based access control permission levels. This requirement ensures that staff can immediately use standardized reporting templates and that authorized stakeholders can expand the template set safely according to their permissions.

#### REQ-139: Canned Report Title Descriptions

- **Type:** functional
- **Priority:** Should — Hover/pop-up title descriptions improve usability for report selection and comprehension, but the system remains usable without them in an initial release.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-367, C-523, C-524

The system shall display a pop-up description when the user hovers over each title of a canned report or template in the reporting interface. The system shall provide a quick access interface with pop-up descriptions for reports. The system shall provide hover tooltips for report titles in the interface. This requirement is needed by staff users to quickly understand what each canned report or template title represents while browsing and selecting reports.

#### REQ-140: Capacity Metric Configuration

- **Type:** functional
- **Priority:** Should — It is important to enable capacity reporting to match agreed meanings, but capacity reporting can still function in a first release using a default definition of capacity.
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`
- **Derived from candidates:** C-032

The system shall allow administrators to configure which metrics define “capacity.” The configurable metrics shall support administrator-selected definitions such as number of items versus shelf space, physical items versus a configured limit, and circulation volume versus processing capacity. This capability ensures that capacity-based reporting aligns with the consortium’s and libraries’ chosen operational meaning of capacity, which is needed by administrators configuring capacity definitions and by stakeholders interpreting capacity reports.

#### REQ-141: Cataloged In-House Use Count Report

- **Type:** functional
- **Priority:** Should — This report is an important in-house usage summary, but it is not explicitly stated as mandatory by the provided source.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-353

The system shall generate a Cataloged In House Use Count report. The report shall present a count of in-house use for cataloged items as a generated Report. This capability is needed by library staff to obtain summarized reporting on cataloged item in-house use.

#### REQ-142: Check-Out and Renewal Counts

- **Type:** functional
- **Priority:** Should — Accurate individual and cumulative counts across check-out and renewal types are important for reporting, but the system can still be usable with a less granular release approach.
- **Sources:** `early_draft_srs_galecia.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-271, C-718

The system shall count all types of check-out individually and cumulatively, including staff check-out, self check-out, staff renewal, self check-out renewal, online renewal, and OPAC renewal. The system shall provide counts that separately distinguish each check-out and renewal type while also producing an overall cumulative count across all listed types. This requirement is needed by stakeholders who rely on consistent circulation and renewal reporting breakdowns for analysis and decision-making.

#### REQ-143: Circulation Count Reporting

- **Type:** functional
- **Priority:** Should — These circulation-count reports and canned templates are important reporting outputs requested by stakeholders, but the system can be usable without them in an initial release.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-287, C-288, C-291, C-293, C-294, C-380, C-467, C-468

The system shall generate a Check in Count circulation report. The system shall generate a Checkout Count circulation report that includes checkouts only, and a Renewals Count report. The system shall generate a circulation report that includes total circulation combining checkouts, renewals, and Uncataloged material circulation, and shall generate a Total Circulation Count report by merging category and Uncataloged material circulation data. The system shall retrieve total circulation including checkouts, renewals, and Uncataloged material and display a breakdown showing those circulation types, and shall include canned reports for Checkout Count and Renewals Count.

#### REQ-144: Collection Age Reporting

- **Type:** functional
- **Priority:** Should — Age of collection reporting is important for collection analysis, but only by call number is explicitly supported in one candidate, making it non-essential for an initial release.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-321, C-496

The system shall generate an Age of collection Report by call number and by shelving location. The system shall also provide an Age of collection Report by call number when requested. This capability supports stakeholders who need to analyze how old the collection is for reporting and decision-making purposes.

#### REQ-145: Comparative Report Columns

- **Type:** functional
- **Priority:** Should — Comparative columns are important for circulation trend analysis, but the system can still be acceptable without them in an initial release.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-373

The system shall support report output formatting that produces comparative columns for time periods and related percent differences. The system shall allow a report result set to include columns for last month's circs and previous month's circ, and a column for the percent difference. The system shall also support comparative month and year columns such as the previous year's month and percent difference between the last month and last year's month. This capability is needed by stakeholders to analyze circulation trends across comparable periods using consistent report column structures.

#### REQ-146: Data Quality Issue Reports

- **Type:** functional
- **Priority:** Should — Staff need data quality reports to assess and correct catalog issues, but the system may still be usable without this capability in an initial release.
- **Sources:** `interview_cataloging_2009-05-08.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Derived from candidates:** C-575, C-656

The system shall provide data quality reports that identify items with invalid item types, items with long call numbers, and bibliographic records with no item records. The system shall provide these data quality reports to help staff assess and correct data issues. The reports shall support data quality assessment by surfacing the specific data conditions of invalid item type, call number length, and missing associated item records for bibliographic records. This requirement is needed by staff who require actionable visibility into catalog data problems to correct them.

#### REQ-147: Deleted Last Copy Reporting

- **Type:** functional
- **Priority:** Should — It supports a specific operational need (external catalog updates and last-copy deletion reporting) but is not stated as mandatory for core system acceptability.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-313, C-377, C-392

The system shall generate a Last Copy Report listing items that were the last copy owned by the Library and that were deleted. The system shall provide this list of deleted last-copy items so it can be used to update external catalogs such as WorldCat. The system shall allow running a report on deleted items that were the last copy in the facility. This capability is needed by library staff and catalog maintenance stakeholders to audit deletions and support external catalog synchronization.

#### REQ-148: Dropdown Regular Expression Query

- **Type:** functional
- **Priority:** Should — Staff need regular-expression selection and matching options in report query filtering, but one proposed source indicates it is not mandatory for an initial release.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-207, C-418, C-465

The system shall allow staff to select regular expressions from a dropdown in the query interface. The system shall provide regular-expression matching options that are selectable from the same dropdown. The system shall provide regular expression support for report query filters so staff can use regular expressions in filtering. This capability is needed by staff to build and refine report queries using regular expressions.

#### REQ-149: Exclude Renewals from Check-In

- **Type:** functional
- **Priority:** Should — Accurate check-in timing in reports is important for reliable circulation reporting, but the system may still be usable with a workaround while the explicit separation is implemented.
- **Sources:** `evergreen_reference_2009.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-537, C-744

The system shall record check-in date/time separately from renewal timestamps so that check-in excludes renewals. The system shall ensure check-in date/time values shown in reports do not include renewals unless explicitly requested. This requirement ensures reporting accuracy for stakeholders who rely on correct separation between check-in events and renewal events, preventing renewals from inflating or contaminating check-in reporting.

#### REQ-150: Financial Transaction Reports

- **Type:** functional
- **Priority:** Should — These reporting outputs are important for financial oversight of patrons and transactions, but the sources are marked proposed and do not indicate mandatory legal or security requirements.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-356, C-357, C-358, C-359, C-360, C-480, C-481, C-482, C-509

The system shall generate a Bills currently Owed by Patrons report. The system shall generate reports of Detailed Payments Received. The system shall generate a Detailed Forgive, Work, and Goods Payments Received report and a Detailed Voids report. The system shall generate Aged Debt reports and shall include canned report templates for Bills Currently Owed by Patrons, Detailed Payments Received, and Aged Debt. This capability is needed by stakeholders who require financial transaction visibility for reporting on patron balances and payment-related events.

#### REQ-151: Financial Transaction Verification Reporting

- **Type:** functional
- **Priority:** Should — This capability is agreed as necessary for financial transaction oversight, but it is not further constrained here with measurable verification/audit actions beyond tracking and verifying.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-620

The system shall provide reports and tools to track and verify financial transactions. The reports shall support verification of financial transactions as recorded in the system, enabling staff or administrators to review transaction details needed for tracking and verification purposes. The tools shall enable tracking and verification activities for financial transactions so that stakeholders can audit and confirm transaction records. This requirement is needed by stakeholders who manage financial records and require reporting support to verify recorded financial events.

#### REQ-152: Fines and Charges Time-Breakdown

- **Type:** functional
- **Priority:** Should — Financial stakeholders need time-scoped, type-based fine and charge reporting, but the system may be acceptable without it in an initial release if an interim reporting approach exists.
- **Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`
- **Derived from candidates:** C-283, C-402, C-403

The system shall provide reports of fines and charges accrued per configurable time period. The system shall support specified time periods such as last 12 months, year-to-date, and last month. The system shall break down accrued fines and charges in the report by type of charge, including overdue fines, damaged item charges, and lost item charges. This capability is needed by stakeholders who require periodic financial reporting with clear time scoping and category-based breakdowns.

#### REQ-153: Fines Waiver and Payment Tracking

- **Type:** functional
- **Priority:** Should — The agreed sources indicate it is important for budgeting and end-of-month reporting with per-branch visibility, but a workaround may exist for an initial release.
- **Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`
- **Derived from candidates:** C-279, C-407, C-408

The system shall track fines waived and payments made per Library and shall track and present payments collected at each Library so each Library can see payments collected at its location. The system shall support tracking fines waived and payments made per library/location for budgeting and reporting purposes. This requirement is needed by financial and reporting stakeholders to produce end-of-month reports and to enable budgeting and per-branch visibility of payments collected.

#### REQ-154: Historical Reporting Warehouse

- **Type:** functional
- **Priority:** Should — Stakeholders agreed on historical reporting needs, but the reporting warehouse and snapshot-specific requirement were proposed rather than explicitly confirmed as mandatory for the first release.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-388, C-517, C-535, C-705, C-706, C-735

The system shall provide historical reporting using a reporting warehouse so that data can be acquired for a given date or date range. The system shall support historical reporting in the form of time-based reports and historical reports. The system shall provide historical snapshot reporting that shows data as it appeared on a specific past date, regardless of subsequent shelving location changes. These capabilities are needed by stakeholders who require answers to questions about what the data looked like on a specific past date or for a specified time period.

#### REQ-155: Hold Management Reports

- **Type:** functional
- **Priority:** Should — The candidate Reports are important for operational hold management but are not stated as mandatory or agreed in the provided sources (all are proposed).
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-345, C-346, C-347, C-349, C-350, C-351, C-506, C-507, C-508

The system shall generate a Report of Items Sent for Holds and a Report of Items Received for Holds. The system shall generate a Holds Purchase Alert Report and an Unfilled Holds Report. The system shall generate a Stale Holds Report for holds sitting on the hold shelf waiting for pickup for too long, and it shall generate an Annual number of holds placed Report. These Reports are needed by stakeholders to manage and monitor the end-to-end hold lifecycle and identify issues such as unfilled and stale holds, as well as track holds placed over time.

#### REQ-156: In-Transit Direction Reports

- **Type:** functional
- **Priority:** Should — Directional in-transit reporting is important for delivery coordination, but it is not explicitly stated as mandatory in the provided sources.
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Derived from candidates:** C-316, C-354, C-355, C-658

The system shall generate in-transit item reports to support delivery coordination between Library branches. The system shall generate a report listing items in transit that includes both the sending Library and the destination Library. The system shall also generate an “Items In Transit to Destination Library” report. The system shall also generate an “Items In Transit by Sending Library” report. This capability is needed by delivery coordination stakeholders to monitor and manage item flow directionally between branches.

#### REQ-157: In-Transit Holds Periodic Reports

- **Type:** functional
- **Priority:** Should — Periodic visibility into in-transit items with outstanding holds is important for operational tracking and decision-making, but it can be deferred depending on release scope.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-218

The system shall generate periodic reports of in-transit items that have outstanding holds. Each generated report shall include in-transit items with outstanding holds as the report contents. This requirement is needed by staff and reporting stakeholders who require recurring visibility into items currently in transit and still subject to holds.

#### REQ-158: Inactive Patron Report Scope

- **Type:** functional
- **Priority:** Should — Scoping and branch-level aggregation are important for making inactive patron reporting usable at operational levels, though the system could still be acceptable with a limited fixed scope in an initial release.
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Derived from candidates:** C-153, C-154, C-155, C-156

The system shall allow the inactive-patrons list to be generated at selectable organizational levels, including System, Home Library, and County. The system shall support configuring additional organizational/grouping levels beyond the built-in ones as needed. When generating the report, the system shall aggregate and report counts of inactive patrons by branch to show which branches have the most inactive patrons. The system shall also allow filtering the inactive-patrons list to a Home Library so branch staff can receive branch-specific cleanup lists and assign tasks. This requirement is needed by reporting stakeholders to ensure inactive patron reporting can be scoped to the appropriate organizational levels and used by branch staff to drive targeted outreach and cleanup.

#### REQ-159: Inactive Patron Reporting Interval

- **Type:** functional
- **Priority:** Should — This is an agreed reporting function but largely depends on how broader “inactive patron” reporting is delivered (scope, fields, and export are covered elsewhere).
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`, `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-145, C-146, C-147, C-148, C-265, C-342, C-504

The system shall generate a list of patrons with no circulation or electronic activity in the last X days, where X is configurable. The system shall allow administrators to specify X (days) to define “inactive” as a fully customizable interval. The system shall also provide common preset inactivity ranges (e.g., 30, 90, 180, and 365 days) to simplify report configuration. This capability is needed by reporting stakeholders to identify and review inactive patrons based on a configurable time window.

#### REQ-160: Invalid Item Type Periodic Reports

- **Type:** functional
- **Priority:** Should — Ongoing reporting of invalid item types is important for operational oversight, but it is not defined as mandatory by the provided source and may be deferred in favor of other reporting requirements.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-217

The system shall generate periodic reports of items that have an invalid item type. The periodic reports shall include all items whose item type is invalid. This capability is needed by stakeholders who require ongoing visibility into catalog or item classification issues to support timely review and remediation.

#### REQ-161: Invalid Patron Home Library Reports

- **Type:** functional
- **Priority:** Should — Periodic invalid home Library reporting is important for data quality monitoring, but the initial release can be acceptable without it if an alternative reporting or manual remediation process exists.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-224

The system shall generate periodic reports listing patrons whose home Library is invalid. Periodic reports shall include the set of patrons with an invalid home Library, based on the system’s patron data. This requirement is needed by stakeholders who require data-quality visibility and ongoing monitoring of patron home Library assignment status.

#### REQ-162: Item Activity Count and Lists

- **Type:** functional
- **Priority:** Should — This set of canned item activity, checkout, and weeding Reports is important for reporting workflows, but no evidence indicates it is mandatory for the first release.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-302, C-303, C-304, C-305, C-306, C-308, C-311, C-312, C-314, C-317, C-319, C-379, C-471, C-472, C-473, C-488, C-491, C-493, C-494, C-495

The system shall generate Reports for item activity including an Items Added Count report, an Items Deleted Count report, an Items Edited Count report, and an Items Count report for total item counts. The system shall also generate item list Reports including a List of Items Added report, a report listing Items currently checked out, a List of Items by Creation Date Range report, and Claims Returned report. The system shall support weeding and threshold-based item list Reports by generating a report listing items with a total use count greater than a specified threshold and a report listing items with a total use count less than a specified threshold for weeding purposes, and it shall generate a weeding report including date of last circulation and number of circulations for items. The system shall provide item use count Reporting by generating item total use counts and use counts broken down by usage date range (for example, fiscal year use count and monthly use count).

#### REQ-163: Items by Fines-Stopped Reason Reports

- **Type:** functional
- **Priority:** Should — This reporting is important for fine-related operational visibility but is not stated as mandatory (sources are only “proposed”), so it can be deferred if necessary.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-307, C-489

The system shall generate a Report listing Items by fines stopped reason. The report shall be provided as a list grouped or organized according to the fines stopped reason, using the “Items by Fines Stopped Reason” reporting content defined in the requirements evidence. This capability is needed by stakeholders who require visibility into which Items are associated with specific fines stopped reasons for reporting and analysis of financial outcomes tied to Items.

#### REQ-164: Items Without Recent Checkout

- **Type:** functional
- **Priority:** Should — It provides useful recurring insight for collection and circulation monitoring, but the system can be acceptable without it in an initial release.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-215

The system shall generate periodic Reports of items that have not been checked out in X days, where X is configurable. The reporting period shall be established by the system’s recurring report mechanism so that the items meeting the “not checked out in X days” criterion are included each time the periodic Report is generated. This requirement enables stakeholders to identify items with potentially stale circulation and support collection management decisions based on checkout recency.

#### REQ-165: Large Libraries Overview Usability

- **Type:** non-functional
- **Priority:** Should — The requirement addresses a clear usability risk for large Library counts, but it was deferred and does not replace other reporting requirements in scope.
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`
- **Derived from candidates:** C-029

The system shall provide presentation options or controls to handle an overview with a large number of Libraries (e.g., 286) so the overview does not become unusable when the set of Libraries would otherwise become crowded. This capability is needed to ensure staff can effectively view a branch overview at consortium scale without the display degrading due to excessive Library count.

#### REQ-166: Last Circulation Date Reporting

- **Type:** functional
- **Priority:** Should — Last circulation date on item reports is important for accurate item usage reporting, but it can be deferred if circulation reporting is otherwise acceptable without a dedicated separate field in the initial release.
- **Sources:** `evergreen_reference_2009.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-536, C-743

The system shall include a field indicating last circulation date for items that is separate from last edit date. The system shall provide an indicator of the last circulation date on item reports. This capability is needed by stakeholders who require item reporting to reflect the most recent circulation rather than the most recent metadata edit.

#### REQ-167: Long Call Number Periodic Report

- **Type:** functional
- **Priority:** Should — Periodic long call number reporting is an important reporting capability, but it is not explicitly stated as mandatory for initial system acceptability.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-221

The system shall generate periodic reports of items that have a long call number. The periodic reports shall include the set of items with a long call number. This requirement enables stakeholders to monitor and review items requiring attention due to their long call number classification through scheduled reporting.

#### REQ-168: MARC Field Consolidated Reporting

- **Type:** functional
- **Priority:** Should — It is important to meet core usability needs for MARC field reporting, but it is not stated as mandatory for an acceptable first release.
- **Sources:** `survey_results_2009.txt`
- **Derived from candidates:** C-739

The system shall allow selection of specific MARC fields for reports and shall present the selected MARC field values consolidated per record rather than spread across multiple rows. This enables staff to pull targeted bibliographic information without fragmentation in the report layout. It is needed by reporting stakeholders who require MARC field reporting that is readable and aligns with their expectations for consolidated per-record presentation.

#### REQ-169: Missing Item Trend Analysis

- **Type:** functional
- **Priority:** Should — Trending supports collection management decisions, but it is not explicitly listed as a mandatory reporting dependency in the provided material.
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`
- **Derived from candidates:** C-090

The system shall provide trending information, such as counts over time, to support collection management decisions related to missing or damaged items. The system shall use the missing/damaged data to enable collection management stakeholders to observe changes over time and make decisions accordingly. This capability ensures that stakeholders can analyze trends rather than relying only on static reporting for missing/damaged items.

#### REQ-170: Missing MARC Field Bibliographic Reports

- **Type:** functional
- **Priority:** Should — This is an important reporting function for metadata quality, but it is described only as “proposed” with no explicit mandate, making it suitable for an expected release rather than strictly required first.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-328, C-500

The system shall generate reports listing bibliographic records that are missing specified MARC fields. The report shall be based on identified MARC field criteria, producing a listing of bibliographic records that do not contain those fields. This capability supports stakeholders who need data quality and metadata completeness visibility for bibliographic records. It is needed by reporting stakeholders who require a consolidated view of MARC field omissions across the catalog data.

#### REQ-171: Missing Report Filtering Controls

- **Type:** functional
- **Priority:** Should — These filtering and note capabilities are important for meaningful missing/damaged reporting but are not explicitly stated as mandatory for an initial release.
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-081, C-082, C-563

The system shall allow missing/damaged item reports to be filtered by date ranges, including predefined examples such as last 30 days and last quarter. The system shall include item condition notes in missing/damaged item reports, such as “water damage” or “vandalism”. The system shall allow missing/damaged item reports to be grouped or filtered by shelf location to identify problematic shelves for potential relocation decisions. This requirement is needed by operations and cataloging stakeholders to analyze missing and damaged item patterns accurately and take appropriate actions.

#### REQ-172: On-Demand Report Editing

- **Type:** functional
- **Priority:** Should — It is important for enabling flexible, timely report generation from preset templates, but it may be deferred if a more limited preset-only reporting capability is acceptable for an initial release.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-365

The system shall provide On Demand reports that are preset but allow editing of selection criteria and display options. The system shall enable these preset On Demand reports to be run on demand. This capability ensures stakeholders can generate customized reports when needed without requiring a separate predefined report for every variation, supporting staff reporting workflows that need timely query adjustments and presentation changes.

#### REQ-173: Open Template Query Fields

- **Type:** functional
- **Priority:** Should — It is an important capability for flexible Reporting configuration and usability, but it can be initially supported through narrower, predefined templates in early releases if needed.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-366

The system shall provide an Open Template reporting interface that exposes all attributes associated with circulation, patrons, items, bills, and bibs for filtering and for choosing display attributes. These same attributes available for filtering shall also be available for selection of fields to display in the generated Report. This capability enables staff to configure report query criteria and presentations without being limited to a predefined set of fields. It is needed by staff who create and run flexible Reporting to support different analysis and presentation needs using consistent attribute definitions.

#### REQ-174: Overdue Item Reporting

- **Type:** functional
- **Priority:** Should — Overdue reporting is an expected operational reporting capability, but it can be delivered in a first release with a narrower set of the proposed overdue and view variations.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-289, C-309, C-310, C-318, C-382, C-474, C-490

The system shall generate reports listing items overdue by a configurable number of days. The system shall support overdue reporting views including a daily view, a shelf reading view, and a patron contact information view, and it shall include a canned report format for “Items Overdue by X Days.” The system shall generate an Overdue Materials report for items more than a configurable number of days overdue, and it shall generate reports for items marked longoverdue by the system, including a “List of Long Overdue” report. The system shall allow running reports for pre-overdue, overdue, and holds notices sent. This capability is needed by library staff to identify overdue items, manage collections, and perform patron outreach using patron contact information.

#### REQ-175: Patron Account Balance Queries

- **Type:** functional
- **Priority:** Should — It is an agreed reporting function that staff need for balance-focused analysis, but it can be delivered alongside broader patron balance reporting workflows.
- **Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`
- **Derived from candidates:** C-281, C-400

The system shall allow staff to query patron accounts whose balances are greater than a specified threshold amount (greater than X dollars). The threshold amount shall be provided as part of the query so that only patrons meeting the “greater than X” condition are returned. This capability supports financial reporting needs by enabling staff to identify patrons with balances above an amount of interest for subsequent reporting or review.

#### REQ-176: Patron Activity History Filtering

- **Type:** functional
- **Priority:** Should — Filtering reports by circulation/Transaction inactivity is important for Patron activity analysis, but it is not explicitly stated as mandatory for initial release.
- **Sources:** `conversations/conv_pines023_patron_characteristics.eml`
- **Derived from candidates:** C-142

The system shall allow Report generation to filter Patrons by circulation/Transaction history, including criteria such as patrons who have not checked anything out within a specified time window (for example, 6 months). The system shall support query criteria equivalent to a request such as: show all Juvenile patrons in zip code 30505 who have not checked anything out in the past 6 months. This requirement is needed by stakeholders who need Patron behavior/activity slices for Reporting and analysis of inactive or low-activity accounts.

#### REQ-177: Patron Balance Report Scopes

- **Type:** functional
- **Priority:** Should — This is a core reporting capability for financial oversight, agreed by stakeholders, though it is not explicitly stated as the only reporting scope within the overall reporting set.
- **Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`
- **Derived from candidates:** C-282, C-401

The system shall provide financial reports of patron account balances for each individual Patron, by home Library, and for the entire system. The reports shall support the three aggregation scopes: by patron account, by home Library, and system-wide totals. This requirement is needed by stakeholders who require visibility into patron financial standing at the patron level, across a patron’s home Library, and at consortium-wide scale.

#### REQ-178: Patron Count Reporting

- **Type:** functional
- **Priority:** Should — These reports are important for understanding patron totals and distribution but are largely additive reporting features proposed without explicit agreed mandatory status.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-329, C-330, C-331, C-332, C-333, C-334, C-335, C-336, C-337, C-478, C-479, C-501, C-502

The system shall generate a Patron Count report of total patrons. The system shall include a canned report for total Patron Count. The system shall generate a Patron Added Count by Month report. The system shall generate a New Patron Count report of patrons added the previous month by demographic category. The system shall generate Patron Count reports by age demographic, county, home library, profile group, and by survey answer, including a List of patrons by survey answer. The system shall generate a Patron Count report by county, city, and zip code, and provide Patron Count reports by county, city, and zip code. These reporting capabilities are needed by stakeholders to summarize patron growth and composition across multiple patron characteristics and locations for analysis and oversight.

#### REQ-179: Patron Demographic Analysis

- **Type:** functional
- **Priority:** Should — It is an agreed reporting capability that supports important patron insights, but the requirement is broad relative to other more specific reporting items in this category.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-618

The system shall provide reports and analysis tools to analyze patron demographics and patron interests. Reports and analysis shall be based on aggregated system data related to patrons and present results in support of demographic and interest insights. This capability is needed by stakeholders who require understanding of patron characteristics to inform service decisions and reporting needs.

#### REQ-180: Patron Expiration and Status Reports

- **Type:** functional
- **Priority:** Should — These reports are important for routine patron and staff account management and security oversight, but they are not explicitly stated as mandatory and can be delivered in an incremental release.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-339, C-341, C-343, C-344, C-505

The system shall generate reports that list patrons by expiration date. The system shall also generate a report listing patrons who are BARRED. In addition, the system shall generate a report listing staff accounts with the date of last password change and the account expiration. The system shall generate a report listing patrons with specific wording in their notes, and the system shall provide a report of Staff Accounts including date of last password change. This set of reports supports staff needs for account lifecycle monitoring, security-related oversight, and identification of patrons requiring attention based on status or notes.

#### REQ-181: Periodic Holds Reports

- **Type:** functional
- **Priority:** Should — Recurring hold reporting is an important expected reporting function, but the system can remain acceptable in an initial release without it if an alternative manual reporting approach exists.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-214, C-216

The system shall generate periodic reports that list bibliographic records with holds and that also generate periodic reports of item-level holds. Periodic reporting shall include both the bibliographic record view of holds and the item-level view of holds. This capability is needed by Library stakeholders and reporting users to routinely monitor hold activity at both the bibliographic and item granularity for operational awareness and decision-making.

#### REQ-182: Periodic Missing Item Reports

- **Type:** functional
- **Priority:** Should — Periodic reporting of missing items is important for ongoing oversight, but it can be deferred if initial releases provide only on-demand missing-item reporting.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-222

The system shall generate periodic reports of missing items for each Library or system scope. Each generated report shall include Missing items data aggregated by the selected scope (per branch/Library or system). This requirement ensures stakeholders can consistently monitor missing items over time using scheduled Reporting outputs rather than ad hoc queries, supporting operational oversight for Libraries and consortium administration.

#### REQ-183: Pivot-Ready Report Output

- **Type:** functional
- **Priority:** Should — Pivot-ready output is important for downstream analysis workflows, but the system can still produce reports without this feature in an initial release.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-383, C-515, C-752

The system shall support pivot table output for report results. The system shall provide pivot table style output for report results. The system shall be able to produce report output suitable for pivot table analysis, including pivot-ready export output. This capability is needed by stakeholders who want to analyze generated report results using pivot table techniques.

#### REQ-184: Query Boolean Operators

- **Type:** functional
- **Priority:** Should — It is an agreed feature that enables more advanced query logic for reporting, but it is not explicitly indicated as mandatory for initial system acceptability.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-208, C-419, C-463

The system shall support Boolean operators (e.g., AND, OR, and NOT) during query construction, enabling staff to build queries beyond simple filters. The system shall provide a full range of Boolean operators for constructing queries. This capability is needed by reporting users to express more complex query logic when generating Reports and retrieving relevant data.

#### REQ-185: Record Relationship Joins

- **Type:** functional
- **Priority:** Should — Join support between related record types is important for producing meaningful cross-entity reports, but the system may still be usable with limited or manual correlation in an initial release.
- **Sources:** `evergreen_reference_2009.txt`
- **Derived from candidates:** C-542

The system shall support joins between record types following key relationships, including bibliographic_record to item via asset.copy and item to action.circulation via circulation transactions. These joins shall enable report generation that combines related data across the specified record types using the defined key relationships. This capability is needed by staff responsible for Reporting to create reports that derive insights from related bibliographic, item, and circulation data without requiring manual correlation outside the system.

#### REQ-186: Recurring Report Selection Editing

- **Type:** functional
- **Priority:** Should — Editing recurring report selections and recipient email addresses is an important usability requirement to maintain correct recurring reporting, but it is not necessarily essential for the system’s initial acceptability.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-372

The system shall allow users to edit recurring reports by adding or removing report selections and editing the recipient email addresses. This capability shall cover modifications to both the set of selected reports within a recurring report and the email addresses to which the recurring report is delivered. The feature is needed by stakeholders who manage recurring report content and distribution to keep report delivery accurate over time.

#### REQ-187: Relative Date Range Canned Reports

- **Type:** functional
- **Priority:** Should — Relative date ranges for canned reports are important for practical scheduled reporting, but the system could still be acceptable using fixed-date selection in an initial release.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-363

The system shall allow canned reports to run for relative date ranges including yesterday, last week, last month, and last year. The system shall execute the report using data corresponding to the selected relative date range, such that the report reflects the appropriate time period at execution. This capability is needed by stakeholders who require recurring reporting without manually selecting fixed date criteria each time.

#### REQ-188: Report Delivery Recipient Address Book

- **Type:** functional
- **Priority:** Should — An address book is important for usable report delivery configuration, but the system could be workable initially with limited destination handling despite the identified gap.
- **Sources:** `evergreen_reference_2009.txt`
- **Derived from candidates:** C-519

The system shall provide an address book for report delivery destinations, supporting delivery methods such as email and FTP. The address book shall store and manage the destinations used when delivering reports to recipients. This enables staff to configure report delivery destinations without lacking a central destination list. This requirement is needed by stakeholders responsible for reporting operations and report delivery setup.

#### REQ-189: Report Filter Text Upload

- **Type:** functional
- **Priority:** Should — Uploading text-file filter criteria is an important reporting convenience expected by stakeholders, but the system can still be acceptable without it in an initial release.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-381, C-520

The system shall allow users to upload a text file containing filter input, including lists of barcodes and TCNs, for use as filter criteria in reports. The system shall use the uploaded text file contents to filter report results according to the provided barcode or TCN values. This requirement enables users to supply external lists for report filtering, which supports reporting stakeholders who need flexible report criteria without manual entry.

#### REQ-190: Report Queue Position Visibility

- **Type:** functional
- **Priority:** Should — Queue visibility with position and status is important for user confidence and operational follow-up, but the system can remain usable without it in an initial release via other monitoring approaches.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-226, C-439, C-440, C-466, C-544, C-654, C-728, C-746

The system shall allow staff and users to see where their Report is in the execution queue by displaying its position in the queue. The system shall display queue details for submitted Reports, including whether the Report is in the queue, how many Reports are ahead, the submission time, and the status. Queue status shall be shown using the states waiting, running, completed, and failed. This requirement ensures stakeholders can track progress and understand whether a submitted Report is still processing, needed by staff and users who submit or monitor Reports.

#### REQ-191: Report Queue Prioritization

- **Type:** functional
- **Priority:** Should — Prioritized processing of reports is agreed as important for workflow and board-level versus ad-hoc needs, but it is not stated as legally or security mandatory.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-378, C-441, C-442, C-513

The system shall allow reports to be assigned priorities so that higher-priority reports are advanced ahead of lower-priority reports in the processing queue. The system shall also support prioritizing certain types of reports so they are moved to the top of the queue ahead of resource-consuming reports. The system shall allow administrators or authorized roles to assign or change the priority of reports so important reports can jump the queue. This capability is needed by executive stakeholders and operational roles (e.g., directors and staff) to ensure important reports are processed first and to provide the desired queue management behavior.

#### REQ-192: Report Template Cloning

- **Type:** functional
- **Priority:** Should — Template cloning is agreed and important for efficient report authoring and reuse, but it does not appear as a blocking requirement for initial reporting functionality.
- **Sources:** `email_report_features.eml`
- **Derived from candidates:** C-426

The system shall provide a clone feature that creates a new report/template based on an existing one without altering the original. This clone operation shall take an existing template and use it as the source for creating the new template instance. The new report/template must be produced as a separate artifact so that subsequent use does not change the original template. This capability is needed by reporting stakeholders to reuse existing report/template configurations while preserving template integrity.

#### REQ-193: Report Writer Filtering and Sorting

- **Type:** functional
- **Priority:** Should — Filtering across relevant fields with basic sorting is important for practical report authoring, but the system can potentially be usable with limited capabilities in an initial release.
- **Sources:** `evergreen_reference_2009.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-460, C-738

The system shall provide basic filtering and sorting capabilities in the report writer interface. The system shall allow filtering reports by all relevant fields and not restrict filtering to a limited subset. These capabilities ensure stakeholders can narrow report results accurately across the applicable dataset and control the order of returned information in the report writer interface.

#### REQ-194: Reporting Interface Types

- **Type:** functional
- **Priority:** Should — Providing the three distinct reporting interface types is an important expected capability for the reporting feature set, but it can be phased if a workaround exists.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-361

The system shall provide three reporting interfaces: canned reports, noncanned/on-demand reports, and open template reporting. Each interface shall support selecting attributes for filtering and display, so that users can generate reports based on the chosen attributes. This requirement establishes the available ways to create and run reports that other reporting requirements rely on. It is needed by staff who produce and review reports and by stakeholders defining the reporting capabilities and user experience.

#### REQ-195: Reuse Existing Report Query Tool

- **Type:** assumption
- **Priority:** Should — Reusing the existing report query tool is an important implementation efficiency and consistency goal, but it is explicitly conditional on feasibility and can be worked around with a separate approach if needed.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-078

The system shall reuse the existing report query tool for candidate selection where feasible. This applies to using the query builder for candidate selection by leveraging the existing report query tool capabilities rather than introducing a separate querying mechanism. The intent is to reduce duplication of query-building functionality while still supporting candidate selection needs within reporting. Stakeholders who maintain the reporting query tooling and depend on consistent query behavior for candidate selection need this to improve reuse and implementation efficiency.

#### REQ-196: Scheduled Inactive Patron Report

- **Type:** functional
- **Priority:** Should — Periodic, no-manual execution for scheduled inactive-patrons reporting is important for routine database maintenance, but it can be worked around with manual runs in an initial release.
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Derived from candidates:** C-169

The system shall support scheduling the inactive-patrons report to run periodically (for example, quarterly) without manual intervention. The system shall enable this scheduled execution so that staff can perform routine cleanup of the patron database on an ongoing basis. This requirement ensures that the inactive-patrons report can be executed reliably and consistently at the agreed cadence, meeting operational expectations expressed by stakeholders who run it quarterly.

#### REQ-197: Scheduled Report Execution Options

- **Type:** functional
- **Priority:** Should — Recurring and time-based report scheduling is important for automated reporting workflows, but the system can be acceptable with limited scheduling capabilities in an initial release.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-369, C-510, C-518, C-545, C-714, C-731

The system shall allow scheduling reports to run either immediately using a Run ASAP option or automatically on a configurable recurring schedule. The configurable recurring schedule options shall include hourly, daily, weekly, monthly, and yearly intervals, and users shall be able to select the applicable scheduling option(s). The system shall also support scheduling reports to run at specified times and shall allow users to cancel a scheduled or running report. This capability is needed by stakeholders who require reliable, automated report generation and timely execution without manual initiation.

#### REQ-198: Shared Saved Query Templates

- **Type:** functional
- **Priority:** Should — Sharing saved query templates improves reporting efficiency and consistency, but the system remains usable if sharing is deferred to a later release.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-056

The system shall allow saved queries to be shared among users as templates. This capability shall treat shared saved queries as reusable templates that other users can use for reporting. The system shall support sharing and saving query templates to enable reuse of report query criteria across users. This requirement is needed by users to efficiently create and standardize reporting queries without rebuilding them each time.

#### REQ-199: Shelf Space Date Range Filtering

- **Type:** functional
- **Priority:** Should — This is an important usability enhancement for time-based comparisons, but it is not explicitly stated as mandatory for initial report acceptability.
- **Sources:** `conversations/conv_pines016_shelf_space.eml`
- **Derived from candidates:** C-048

The system shall allow users to filter the Shelf Space Report by an arbitrary date range so they can compare shelf space utilization across periods (for example, comparing Q1 versus Q2). This filtering capability shall apply to the Shelf Space Report and use the selected date range as the filter criterion. The rationale is to support staff and stakeholders who need time-based shelf space comparisons for analysis and reporting.

#### REQ-200: Staff Productivity and Workflow Reports

- **Type:** functional
- **Priority:** Should — It is an agreed reporting capability for analyzing staff productivity and workflow, but it is not specified with measurable acceptance criteria in the provided material.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-619

The system shall provide Report and analysis tools to analyze staff productivity and workflow. The tools shall support analyzing staff productivity and workflow by generating reports from queried and aggregated system data. This capability is needed by staff and administrators to understand how work processes are performing and to support operational review and improvement.

#### REQ-201: Survey Response Counts by Week

- **Type:** functional
- **Priority:** Should — The reports and survey-name filtering are important for providing usable voter survey response reporting, but they were not explicitly stated as mandatory in the source set.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-338, C-340, C-391, C-503, C-710

The system shall generate Voter Survey Responses count reports by week, including a county breakdown for the Voter Survey Responses by county by week reports. The system shall also generate Voter Registration survey responses count reports by week. The system shall provide reporting for Voter Survey Responses. The reporting shall support filtering by survey name, where the system resolves survey names to survey identifiers internally rather than requiring entry of a survey id.

#### REQ-202: Transaction Dimension Grouping

- **Type:** functional
- **Priority:** Should — The requested grouping dimensions are important for backroom statistics and busy-period identification, but they are not described as legally or security mandatory.
- **Sources:** `early_draft_srs_galecia.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-267, C-716, C-742

The system shall allow transactions to be grouped by hour, terminal, branch, and system for backroom statistics. The system shall support transaction grouping by hour to facilitate identification of busy periods. This requirement ensures reporting stakeholders can analyze circulation or financial Transaction patterns by the specified dimensions for backroom statistics and operational workload insights.

#### REQ-203: Transaction Type Reporting

- **Type:** functional
- **Priority:** Should — Transaction type breakdown and type-filtered querying are important for meaningful reporting, but they can be deferred without blocking initial overall transaction statistics reporting.
- **Sources:** `early_draft_srs_galecia.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-268, C-269, C-740

The system shall record and report transaction types including check-ins, check-outs, fines collected, and patron registrations. The system shall include these transactions in statistics and queries. The system shall allow queries of all transactions or filtering results by specific transaction type. This requirement is needed by stakeholders who require transaction type visibility for reporting and analysis of circulation and financial events.

#### REQ-204: Uncataloged Circulation Statistics

- **Type:** functional
- **Priority:** Should — Counting and reporting uncataloged material transactions is important for complete circulation statistics, but it can be deferred if initial releases focus on cataloged-only reporting.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-243, C-554, C-292, C-352, C-469

The system shall count transactions for uncataloged material and include those transactions in circulation statistics and reports. The system shall generate a Non-Cat Count circulation report. The system shall generate a NonCat In House Use Count by month report. The system shall include a canned report for Non-Cataloged Count. This requirement is needed by stakeholders responsible for circulation statistics and reporting to ensure uncataloged material usage is reflected in standard and canned reports.

#### REQ-205: Uncataloged Material Usage Reporting

- **Type:** functional
- **Priority:** Should — Understanding and analyzing uncataloged material usage is important for reporting and assessment, but it is not defined as mandatory in the provided sources.
- **Sources:** `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`
- **Derived from candidates:** C-242, C-553

The system shall provide the ability to identify how uncataloged material is being used and shall record how uncataloged materials are being used so that usage can be analyzed. This supports reporting needs for stakeholders who require visibility into uncataloged material usage patterns in order to evaluate and analyze usage over time.

#### REQ-206: User-Saved Report Definitions

- **Type:** functional
- **Priority:** Should — Saving and reusing report definitions and queries is an important usability expectation for repeated reporting, but it is not explicitly indicated as mandatory in the provided sources.
- **Sources:** `evergreen_reference_2009.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-462, C-732

The system shall allow Users to save report definitions and reuse them for later report runs. The system shall also allow Users to save queries and reuse them for repeated report runs. This requirement enables Users to avoid reconfiguring report definitions and queries when generating the same reports multiple times, improving staff efficiency and reporting consistency for stakeholders who run repeated reports.

#### REQ-207: Weeding Reports

- **Type:** functional
- **Priority:** Should — Weeding reports are expected to support regular branch collection maintenance, but the requirement does not indicate they are mandatory for initial system acceptability.
- **Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Derived from candidates:** C-660

The system shall provide weeding reports to assist branch staff in collection maintenance. These reports are intended to be used frequently, supporting ongoing branch activities related to deciding what materials to weed. The functionality is needed by branch staff to maintain collection quality and support collection maintenance processes.

#### REQ-208: Branch Capacity Color-Coding

- **Type:** functional
- **Priority:** Could — Color-coded status is a usability enhancement for Branch Capacity reporting, but the system can still be acceptable without this visual mapping in an initial release.
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`
- **Derived from candidates:** C-031

The system shall support color-coding of branch capacity status using a defined mapping of green for under capacity, yellow for getting full, and red for at/over capacity. This requirement ensures that capacity status is immediately understandable to stakeholders reviewing branch capacity information in reports.

#### REQ-209: Circulation Breakdown Reports

- **Type:** functional
- **Priority:** Could — While multiple breakdown report variants are proposed, none are marked as agreed or mandatory and availability is noted as partially available or not available for several breakdown dimensions.
- **Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`
- **Derived from candidates:** C-290, C-295, C-296, C-297, C-298, C-299, C-300, C-301, C-470, C-483, C-484, C-485, C-486, C-487

The system shall generate circulation count reports broken down by circulation modifier and by category fields (Cat1, Cat2 such as Adult, YA, Juv). The system shall also generate circulation count reports grouped by Dewey call number ranges, and by shelving location. The system shall further generate circulation count reports by MARC fields, and by circulation location broken down by patron county and patron home library. The system shall provide a circulation count report broken down by patron age demographic. These reports are needed by stakeholders who require circulation breakdown analysis across item and patron dimensions to support reporting and management decisions.

#### REQ-210: Hold Type Subtotaling

- **Type:** functional
- **Priority:** Could — This provides useful reporting detail but is not explicitly required beyond existing transaction and reporting capabilities.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-275

The system shall subtotal holds by type in transaction reports. The hold types shall include active, frozen, and frozen-until holds. This enables stakeholders to view transaction reporting with hold type breakdowns, supporting clearer hold management reporting needs.

#### REQ-211: Interlibrary Loan Reporting

- **Type:** functional
- **Priority:** Could — Generating IntraPINES Loans reports by system and facility is useful for analysis, but it is only listed as a proposed capability with no explicit mandatory commitment.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-348

The system shall generate IntraPINES Loans reports for all systems and additionally by system and by facility. The generated reports shall support the scopes “all facilities” and “by facility” in addition to “all systems” and “by system.” This capability provides staff with the necessary Interlibrary Loan Reporting views to understand loan activity at both consortium-wide and more granular organizational levels.

#### REQ-212: Patron Behavior and Usage Analytics

- **Type:** functional
- **Priority:** Could — The need for patron behavior analytics is stated but only as proposed examples of analytics, without indication of mandatory scope or calculations beyond illustrative metrics.
- **Sources:** `early_draft_srs_galecia.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-229, C-230, C-231, C-232, C-723

The system shall produce statistics and analytics that can be used to understand and predict patron behavior and material usage. The system shall compute, for a particular Item, how quickly that Item is returned on average. The system shall compute, for a particular Item, the likelihood that the Item will be renewed. The system shall compute what percent of check-outs at a Library are renewals. This capability is needed by stakeholders who want analytics (for example renewal likelihood and percent renewals) to support understanding and prediction of patron behavior and how materials are used.

### 3.5 Security & Access

#### REQ-213: Accounting and Audit Compliance

- **Type:** constraint
- **Priority:** Must — This is an essential compliance constraint covering auditing and accounting requirements for reports and archived data.
- **Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`
- **Derived from candidates:** C-277, C-411

The system shall ensure that all Report generation and all data archiving comply with standard accounting practice and with state, county, and municipal auditing requirements. This compliance shall apply to the content and storage of the archived data used to support reporting and audit needs. The rationale is to meet financial oversight obligations and expectations of organizations and oversight stakeholders responsible for accounting and audits.

#### REQ-214: Administrative Data Access Controls

- **Type:** functional
- **Priority:** Must — Access restriction for both database data structures and the query tool is essential to meet the system’s Security & Access goals.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`
- **Derived from candidates:** C-209, C-420

The system shall provide administrative controls that allow administrators to restrict staff access to database tables and to individual fields. The system shall also provide administrative controls to restrict access to the query tool. These controls shall support limiting who can view or query specific data and which staff can use querying capabilities. This requirement is needed by administrators and security stakeholders to ensure appropriate access governance for reporting and system data access.

#### REQ-215: Authorized Financial Record Editing

- **Type:** functional
- **Priority:** Must — Editing financial information is essential for system operation and must be controlled to protect security and integrity of financial records.
- **Sources:** `early_draft_srs_galecia.txt`
- **Derived from candidates:** C-280

The system shall allow financial information to be updated by authorized staff. Access to update financial information shall be restricted to users with appropriate authorization based on Role-based access control. The system shall record that an authorized update occurred as part of the financial record editing process, enabling Security & Access monitoring of changes. This requirement is needed by authorized staff to maintain accurate financial information while ensuring that only permitted staff can alter sensitive financial data in the Library Automation System.

#### REQ-216: Automatic Report Permissions Update

- **Type:** functional
- **Priority:** Must — Automatic permission updates on role change are essential to correct role-based access control for report access and therefore are required for system security.
- **Sources:** `email_report_features.eml`
- **Derived from candidates:** C-430

The system shall support role-based administration so that when a user’s role is changed (for example, from Staff to Manager), the user’s report permissions are updated automatically according to the assigned role. This requirement ensures that role changes immediately take effect for authorization to access Reports, reducing the risk of incorrect or outdated permissions and supporting the security needs of administrators and security stakeholders.

#### REQ-217: Confirm Purge Deletions

- **Type:** constraint
- **Priority:** Must — A separate confirmation step is an agreed security control that helps prevent accidental purge deletions, making it essential for acceptable administrative operations.
- **Sources:** `conversations/conv_pines021_item_purging.eml`
- **Derived from candidates:** C-109

The system shall require a separate confirmation step before performing any actual deletion of items or records identified for purge. This confirmation step shall be completed prior to initiating the deletion operation, so that purge deletions cannot be executed as an immediate consequence of selection or identification. This requirement is needed to reduce the risk of unintended data loss and to provide an explicit safeguard for staff users performing administrative purge actions.

#### REQ-218: Deletion audit actor fields

- **Type:** functional
- **Priority:** Must — Storing deletion audit records with actor identity, time, and affected record details is essential for security auditing and accountability.
- **Sources:** `conversations/conv_pines022_deletions.eml`
- **Derived from candidates:** C-115, C-116, C-117, C-118, C-119, C-120

The system shall store deletion audit records that include record_type, record_id, deleted_by, deleted_at, and a field capturing the performing user’s Library or branch. The system shall record the type of record deleted in the deletion audit entry (e.g., item, patron, bib, other). The system shall record the timestamp (deleted_at) for each deletion event in the audit table. The system shall record the identity of the user who performed each deletion (deleted_by) and the performing user’s Library or branch for that deletion event. The system shall store the identifier (record_id) of each deleted record so specific records can be referenced, supporting security auditing and accountability for stakeholders responsible for access control and audit compliance.

#### REQ-219: Deletion audit capture

- **Type:** functional
- **Priority:** Must — Auditability of deletion actions (including denied attempts) is an agreed core security requirement essential for later review and accountability.
- **Sources:** `conversations/conv_pines022_deletions.eml`
- **Derived from candidates:** C-113, C-114, C-127

The system shall log every successful deletion event to an audit table so deleted records are retained for later review. The system shall implement a database trigger that captures deletion events and writes them to the audit table. The system shall also log attempted deletions that were denied due to failed authorization or validation to the audit trail. This capability is needed by stakeholders responsible for security auditing, incident review, and accountability for deletion activity.

#### REQ-220: Deletion Authorization Permissions

- **Type:** functional
- **Priority:** Must — Restricting deletions to explicitly authorized users is essential security and safety control to prevent accidental mass deletion.
- **Sources:** `conversations/conv_pines021_item_purging.eml`
- **Derived from candidates:** C-111

The system shall restrict the ability to perform deletions to users with explicit authorization/permissions to prevent accidental mass deletion. Deletion actions shall therefore require the user to be explicitly permitted before the system allows records to be deleted. This requirement is needed to make the system safe against unintended data loss and to protect stakeholders’ cataloged and administered holdings from accidental purge behavior.

#### REQ-221: Demographic Report De-identification

- **Type:** non-functional
- **Priority:** Must — Because demographic statistics must not expose personally identifiable information and identifying elements must be deleted, this privacy/anonymization control is essential for acceptable system security and compliance.
- **Sources:** `early_draft_srs_galecia.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-234, C-722

The system shall anonymize demographic data used for statistics by deleting information that could be used to identify a patron. The system shall anonymize demographic statistics produced in demographic reports to ensure that no personally identifiable information is exposed. This anonymization requirement applies to the demographic data used as the basis for statistical outputs, ensuring that identifying elements are removed prior to report generation. Stakeholders including security and privacy reviewers need this control to reduce the risk of patron re-identification from demographic reporting.

#### REQ-222: Indirect OPAC Patron Access

- **Type:** constraint
- **Priority:** Must — This constraint is essential to prevent unauthorized direct system use by Patrons and to establish a secure access boundary for the OPAC experience.
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-679

The system shall provide only indirect Patron access through OPAC displays, ensuring that Patrons are not direct Users of the Library Automation System. Any Patron interaction with system functionality shall occur via OPAC views rather than through authenticated staff or administrative system functions. This access boundary is required to enforce the separation between Patron-facing discovery/requests and protected system operations, supporting overall security and alignment of access behaviors across the consortium.

#### REQ-223: Local System Administrator Configuration

- **Type:** functional
- **Priority:** Must — Local unit configuration by Local System Administrators is explicitly agreed and is essential for meeting the consortium’s access and administration model.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-622

The system shall allow Local System Administrators to configure the system locally for their organizational units. This requirement ensures that administrators responsible for specific organizational units can manage system configuration without relying on Global Administration, addressing the operational needs of Local System Administrators and the organizational governance expectations of participating units.

#### REQ-224: Purge audit trail logging

- **Type:** functional
- **Priority:** Must — An audit trail for purge actions is essential to accountability and security monitoring and was explicitly agreed.
- **Sources:** `conversations/conv_pines021_item_purging.eml`
- **Derived from candidates:** C-110

The system shall maintain an audit trail of all purge-related actions, recording who performed the purge, what was purged, and when the purge occurred. This audit trail shall capture the purge actions so stakeholders can track purge accountability and timing for security and compliance needs.

#### REQ-225: Role-Based Access Control

- **Type:** functional
- **Priority:** Must — This is an agreed security requirement that defines how authorization is controlled and administered across staff, workgroups, and groups.
- **Sources:** `early_draft_srs_galecia.txt`, `email_staff_login.eml`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-181, C-449, C-450, C-452, C-453, C-454, C-597, C-599, C-600, C-601, C-602, C-643, C-673, C-674

The system shall implement role-based access control using security groups and/or roles to control authorization for individuals, workgroups, and arbitrary staff groups. The system shall allow permission control through security groups and/or role assignments. The system shall enable administrators to change a staff member’s permissions by changing the staff member’s role assignment rather than modifying individual permissions, and it shall provide an administration interface that makes it easy to administer roles and permissions. The system shall support definable and assignable roles for staff and allow administrators to create and manage security groups and roles.

#### REQ-226: Role-Based Transfer Permission Control

- **Type:** functional
- **Priority:** Must — Limiting transfer utility access by role is essential to maintain security and prevent unauthorized transfers between libraries.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-066

The system shall restrict access to the transfer utility using role-based access control by limiting transfer capabilities to specified roles. The transfer capability shall be available only to roles such as managers, administrators, and transfer coordinators, and not to every staff member. This requirement ensures that only authorized staff can initiate transfers that change an Item’s holding between libraries. Stakeholders such as library administrators and security reviewers need this control to prevent unauthorized or unintended cross-library transfers.

#### REQ-227: Staff Login Identity Auditing

- **Type:** functional
- **Priority:** Must — At minimum, auditability requires recording the identity of the currently logged-in staff member for security and accountability.
- **Sources:** `email_staff_login.eml`
- **Derived from candidates:** C-448

The system shall track which staff member is logged in for audit purposes. This requirement ensures audit stakeholders can attribute system actions to an identifiable staff member during authenticated use, supporting security oversight and accountability.

#### REQ-228: Transaction Archive Privacy Controls

- **Type:** constraint
- **Priority:** Must — Protecting Patron privacy under applicable State Law and prohibiting personally identifiable information in the archive are essential constraints for system acceptability.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`
- **Derived from candidates:** C-213, C-434, C-436

The system shall archive Transaction data in a manner that protects Patron privacy as defined by applicable State Law and shall comply with that State Law. The system shall archive Transaction records without retaining personally identifiable information in the transaction archive. The system shall still provide useful demographic statistics from the archived Transaction data while maintaining Patron privacy.

#### REQ-229: Transaction History Retention

- **Type:** non-functional
- **Priority:** Must — Retention of transaction history and legally/audit-mandated archives is required to meet security and regulatory compliance obligations.
- **Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`, `email_report_features.eml`, `survey_results_2009.txt`
- **Derived from candidates:** C-266, C-435, C-412, C-715

The system shall maintain transaction history for X days, where X is configurable. The system shall retain monthly aggregate and annual aggregate information indefinitely. The system shall enforce data retention policies required for audits by retaining specified data for seven years where mandated. The system shall retain archived transaction data for the retention period required by State Law, configurable to the legally required number of years. This requirement is needed by security and compliance stakeholders to ensure audit readiness and legal retention of transaction records and aggregates.

#### REQ-230: Transfer Action Audit Logging

- **Type:** functional
- **Priority:** Must — Audit logging of Transfer actions is essential for security accountability and satisfies the explicitly agreed audit requirement.
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Derived from candidates:** C-072

The system shall log all Transfer actions for audit purposes. This logging requirement applies to every Transfer that changes an Item from one Library or other designated destination to another. The audit logs are needed by Security and Access stakeholders to provide traceability of staff or administrative actions involving Item movement.

#### REQ-231: User Class Role-Based Permissions

- **Type:** functional
- **Priority:** Must — Defining role-based access for the required user classes is essential to meet the security and authorization needs of the system.
- **Sources:** `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Derived from candidates:** C-621, C-598, C-675, C-676, C-677, C-678

The system shall support the defined user classes—Patron, Staff, Local System Administrator, Library Manager, Library Director, and Global System Administrator—using role-based access and capabilities. The system shall provide a Global System Administrator role with full system access. The system shall provide a Local System Administrator role with branch-level reporting and configuration privileges. The system shall provide a Library Manager role that can run approved reports and perform limited template modification. The system shall provide a Staff role that can run reports within assigned permissions. This requirement is needed by security and system stakeholders to ensure consistent authorization across interacting user classes and to delegate reporting, configuration, and administrative capabilities appropriately.

#### REQ-232: Fast Staff Login and Switching

- **Type:** non-functional
- **Priority:** Should — Improving staff login speed and switching directly supports operational responsiveness and reduces identified security risks, but the system may remain usable with slower login in an initial release.
- **Sources:** `email_staff_login.eml`
- **Derived from candidates:** C-455, C-456, C-458

The system shall reduce staff login time to minimize service slowdowns during busy periods. The system shall provide mechanisms to reduce security risks such as password sharing and unattended logged-in terminals, including faster login and switching behavior. The system shall allow quick switching between different staff users on shared public service computers so that multiple staff members can use the same terminals throughout the day, such as where 15 public service computers are used by 8 different staff members during the day. This requirement is needed by staff and operations to keep service responsive and by library management to reduce common security risks arising from hurried login and left-unattended terminals.

#### REQ-233: Fine-Grained Report Permission Controls

- **Type:** functional
- **Priority:** Should — Fine-grained report permission controls and shared-folder administration are important for secure and manageable access to reports, but a basic access model may remain usable in an initial release with workaround administration.
- **Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`, `survey_results_2009.txt`
- **Derived from candidates:** C-200, C-201, C-202, C-203, C-427, C-428, C-429, C-528, C-725, C-726, C-727

The system shall implement distinct, fine-grained permission levels that limit who may create, clone, modify, or run reports. The system shall allow administrators to create shared folders that permit or deny staff from running specific reports. The system shall allow administrators to permit or restrict staff from running ad hoc reports on specific sets of data using shared folders or similar constructs. The system shall make report permissions easy to administer. This requirement is needed by administrators and security stakeholders to enforce controlled access to report creation, cloning, modification, running, and ad hoc execution on defined data sets.

#### REQ-234: Global System Administrator Administration

- **Type:** functional
- **Priority:** Should — It is an agreed, security-relevant administrative function but is limited to a specific administrator role and does not replace other access control and reporting permissions requirements elsewhere in the category.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Derived from candidates:** C-623

The system shall allow the Global System Administrator to implement software changes and configurations and to generate statistical reports for PINES as a whole. This capability is needed by administrators who manage consortium-wide operations and require both system configuration control and consolidated statistical reporting across PINES.

#### REQ-235: Staff Login Methods

- **Type:** functional
- **Priority:** Should — Supporting both optional streamlined login and guaranteed username/password fallback improves usability and operational continuity across sites while preserving required authentication behavior.
- **Sources:** `early_draft_srs_galecia.txt`, `email_staff_login.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Derived from candidates:** C-192, C-193, C-194, C-443, C-444, C-445, C-446, C-447, C-457, C-657

The system shall support streamlined staff login methods, such as card swipe using an RFID employee badge, for ILS terminals or staff workstations, while making these streamlined methods optional (supported but not required). The system shall also support traditional individual login credentials consisting of a username and password as an available login method and as a fallback when card-reader hardware is not available. Streamlined login methods shall not bypass individual authentication; the individual’s identity must still be authenticated. The system shall function in locations that do not have card-reader hardware by not requiring card readers to operate the system, enabling staff to authenticate using the supported alternative method. This requirement is needed by staff and operations at varying branch sites to ensure convenient login without weakening authentication security.

#### REQ-236: Staff Role and Permission Administration

- **Type:** functional
- **Priority:** Should — Although important for secure operations and day-to-day administration, it is not explicitly stated as legally mandatory or required for initial usability.
- **Sources:** `email_staff_login.eml`
- **Derived from candidates:** C-451

The system shall provide easy administration of roles and permissions, ensuring that administrative tasks are simple and straightforward. This capability supports Security & Access stakeholders who need roles and permissions to be maintained efficiently and correctly.

#### REQ-237: Optional Deletion Reason Capture

- **Type:** functional
- **Priority:** Could — It is explicitly questioned as usefulness and therefore is an optional enhancement rather than a mandatory security or compliance function.
- **Sources:** `conversations/conv_pines022_deletions.eml`
- **Derived from candidates:** C-129

The system shall optionally capture a reason or the record’s status prior to deletion, where this information is treated as a capability to evaluate usefulness. This optional capture is based on the question of “possibly why (status before deletion?)” and is not required for all deletions. The rationale is to support Security & Access stakeholders in assessing whether recording pre-deletion context is valuable for governance, investigation, or audit-related needs without imposing mandatory data capture.

## 4. Traceability matrix

| Source document | Requirements | Discarded |
|---|---|---|
| `conversations/conv_pines014_material_volume.eml` | REQ-035, REQ-046, REQ-072, REQ-089, REQ-098, REQ-099, REQ-100 | - |
| `conversations/conv_pines015_capacity_interface.eml` | REQ-038, REQ-042, REQ-067, REQ-077, REQ-078, REQ-080, REQ-133, REQ-134, REQ-140, REQ-165, REQ-208 | - |
| `conversations/conv_pines016_shelf_space.eml` | REQ-076, REQ-097, REQ-119, REQ-120, REQ-121, REQ-199 | DIS-001, DIS-002 |
| `conversations/conv_pines018_item_transfer.eml` | REQ-002, REQ-004, REQ-005, REQ-007, REQ-008, REQ-009, REQ-012, REQ-013, REQ-014, REQ-015, REQ-016, REQ-017, REQ-023, REQ-024, REQ-025, REQ-070, REQ-195, REQ-198, REQ-226, REQ-230 | - |
| `conversations/conv_pines019_020_missing_intransit.eml` | REQ-033, REQ-053, REQ-069, REQ-075, REQ-102, REQ-122, REQ-135, REQ-169, REQ-171 | - |
| `conversations/conv_pines021_item_purging.eml` | REQ-001, REQ-003, REQ-006, REQ-010, REQ-011, REQ-019, REQ-020, REQ-021, REQ-028, REQ-217, REQ-220, REQ-224 | - |
| `conversations/conv_pines022_deletions.eml` | REQ-083, REQ-218, REQ-219, REQ-237 | DIS-003, DIS-004 |
| `conversations/conv_pines023_patron_characteristics.eml` | REQ-043, REQ-058, REQ-094, REQ-104, REQ-105, REQ-108, REQ-109, REQ-176 | - |
| `conversations/conv_pines024_inactive_patrons.eml` | REQ-031, REQ-054, REQ-085, REQ-091, REQ-092, REQ-158, REQ-159, REQ-196 | - |
| `early_draft_srs_galecia.txt` | REQ-002, REQ-003, REQ-006, REQ-007, REQ-008, REQ-010, REQ-013, REQ-016, REQ-017, REQ-020, REQ-021, REQ-022, REQ-023, REQ-026, REQ-030, REQ-032, REQ-037, REQ-041, REQ-047, REQ-050, REQ-051, REQ-056, REQ-057, REQ-059, REQ-061, REQ-062, REQ-063, REQ-064, REQ-066, REQ-073, REQ-074, REQ-075, REQ-078, REQ-079, REQ-081, REQ-083, REQ-084, REQ-086, REQ-087, REQ-088, REQ-090, REQ-093, REQ-095, REQ-096, REQ-100, REQ-102, REQ-103, REQ-105, REQ-107, REQ-110, REQ-111, REQ-112, REQ-113, REQ-114, REQ-115, REQ-116, REQ-117, REQ-118, REQ-119, REQ-121, REQ-123, REQ-124, REQ-125, REQ-126, REQ-127, REQ-130, REQ-131, REQ-138, REQ-139, REQ-141, REQ-142, REQ-143, REQ-144, REQ-145, REQ-147, REQ-148, REQ-150, REQ-152, REQ-153, REQ-154, REQ-155, REQ-156, REQ-157, REQ-159, REQ-160, REQ-161, REQ-162, REQ-163, REQ-164, REQ-167, REQ-170, REQ-172, REQ-173, REQ-174, REQ-175, REQ-177, REQ-178, REQ-180, REQ-181, REQ-182, REQ-183, REQ-184, REQ-186, REQ-187, REQ-189, REQ-190, REQ-191, REQ-194, REQ-197, REQ-201, REQ-202, REQ-203, REQ-204, REQ-205, REQ-209, REQ-210, REQ-211, REQ-212, REQ-213, REQ-214, REQ-215, REQ-221, REQ-225, REQ-228, REQ-229, REQ-233, REQ-235 | - |
| `email_financial_reports.eml` | REQ-052, REQ-088, REQ-096, REQ-107, REQ-110, REQ-126, REQ-152, REQ-153, REQ-175, REQ-177, REQ-213, REQ-229 | - |
| `email_report_features.eml` | REQ-073, REQ-084, REQ-087, REQ-111, REQ-113, REQ-114, REQ-115, REQ-116, REQ-118, REQ-127, REQ-148, REQ-184, REQ-190, REQ-191, REQ-192, REQ-214, REQ-216, REQ-228, REQ-229, REQ-233 | - |
| `email_staff_login.eml` | REQ-225, REQ-227, REQ-232, REQ-235, REQ-236 | - |
| `evergreen_reference_2009.txt` | REQ-003, REQ-006, REQ-030, REQ-047, REQ-048, REQ-056, REQ-061, REQ-068, REQ-071, REQ-079, REQ-086, REQ-088, REQ-093, REQ-095, REQ-096, REQ-103, REQ-106, REQ-112, REQ-113, REQ-114, REQ-115, REQ-116, REQ-130, REQ-131, REQ-136, REQ-137, REQ-139, REQ-143, REQ-144, REQ-148, REQ-149, REQ-150, REQ-154, REQ-155, REQ-159, REQ-162, REQ-163, REQ-166, REQ-170, REQ-174, REQ-178, REQ-180, REQ-183, REQ-184, REQ-185, REQ-188, REQ-189, REQ-190, REQ-191, REQ-193, REQ-197, REQ-201, REQ-204, REQ-206, REQ-209, REQ-233 | - |
| `interview_cataloging_2009-05-08.txt` | REQ-002, REQ-003, REQ-006, REQ-007, REQ-010, REQ-013, REQ-016, REQ-017, REQ-018, REQ-020, REQ-021, REQ-022, REQ-023, REQ-026, REQ-027, REQ-075, REQ-083, REQ-100, REQ-101, REQ-102, REQ-119, REQ-146, REQ-171, REQ-204, REQ-205 | - |
| `interview_sysadmin_2009-05-10.txt` | REQ-030, REQ-047, REQ-048, REQ-056, REQ-059, REQ-060, REQ-061, REQ-062, REQ-063, REQ-064, REQ-071, REQ-225, REQ-231 | - |
| `meeting_minutes/meeting_2009-03-15_minutes.txt` | REQ-029, REQ-034, REQ-036, REQ-039, REQ-040, REQ-044, REQ-045, REQ-051, REQ-055, REQ-057, REQ-082, REQ-087, REQ-116, REQ-132, REQ-151, REQ-179, REQ-200, REQ-223, REQ-231, REQ-234 | - |
| `meeting_minutes/meeting_2009-07-20_minutes.txt` | REQ-030, REQ-032, REQ-041, REQ-047, REQ-050, REQ-051, REQ-056, REQ-057, REQ-059, REQ-061, REQ-062, REQ-063, REQ-064, REQ-066, REQ-074, REQ-084, REQ-087, REQ-102, REQ-119, REQ-146, REQ-156, REQ-190, REQ-207, REQ-225, REQ-235 | - |
| `meeting_tech_subcommittee_2009-06-30.txt` | REQ-030, REQ-032, REQ-041, REQ-047, REQ-049, REQ-051, REQ-056, REQ-057, REQ-059, REQ-061, REQ-062, REQ-065, REQ-074, REQ-079, REQ-093, REQ-103, REQ-112, REQ-154, REQ-197, REQ-201, REQ-222, REQ-225, REQ-231 | - |
| `survey_results_2009.txt` | REQ-002, REQ-016, REQ-079, REQ-081, REQ-083, REQ-084, REQ-086, REQ-090, REQ-093, REQ-103, REQ-112, REQ-114, REQ-116, REQ-124, REQ-125, REQ-128, REQ-129, REQ-142, REQ-149, REQ-154, REQ-166, REQ-168, REQ-183, REQ-190, REQ-193, REQ-197, REQ-202, REQ-203, REQ-206, REQ-212, REQ-221, REQ-229, REQ-233 | - |

## 5. Discarded requirements (blacklist)

Requirements identified in the sources but not included in the specification.

#### DIS-001: Branch-manager testing coordination assignment

- **Reason:** out-of-scope
- **Sources:** `conversations/conv_pines016_shelf_space.eml`
- **Candidates:** C-051

Assigning a named individual to coordinate rollout and testing is a project-management responsibility, not a system requirement.

#### DIS-002: Shelf-space estimation investigation assignment

- **Reason:** out-of-scope
- **Sources:** `conversations/conv_pines016_shelf_space.eml`
- **Candidates:** C-052

Assigning a named individual to investigate estimation methods is a project-management responsibility, not a product requirement. The implementable shelf-space estimation capability remains in REQ-120.

#### DIS-003: Deletion-trigger implementation assignment

- **Reason:** out-of-scope
- **Sources:** `conversations/conv_pines022_deletions.eml`
- **Candidates:** C-131

Assigning a named individual to provide a database trigger belongs in a project plan or responsibility matrix, not the product requirements specification.

#### DIS-004: Deletion-report drafting assignment

- **Reason:** out-of-scope
- **Sources:** `conversations/conv_pines022_deletions.eml`
- **Candidates:** C-132

Assigning a named individual to draft detailed report requirements belongs in a project plan or responsibility matrix, not the product requirements specification.


## 6. Quality assurance log

Each iteration is scored (2 × missing candidates + duplicate names + reviewer issues); this document is the version from iteration **3**, which scored best.

| Iteration | Reviewer approved | Missing candidates | Reviewer issues | Score |
|---|---|---|---|---|
| 1 | no | 14 | 16 | 44 |
| 2 | no | 0 | 14 | 14 |
| 3 | no | 0 | 11 | 11 |

**Open reviewer issues for this version (not resolved within the iteration limit):**

- *duplicate* (REQ-056, REQ-048): Both requirements mandate background or queued processing for long-running reports so interactive or production operations are not blocked. REQ-056 is the broader non-disruptive reporting requirement, while REQ-048 repeats the same behavior for long-running reports.
- *duplicate* (REQ-100, REQ-098): REQ-100 already requires category breakdown counts in the Material Volume Report, while REQ-098 separately requires customizable material quantity categories and reporting by category. The overlap is substantial and the boundary between fixed Material Volume categories and configurable categories is unclear.
- *vocabulary* (REQ-057, REQ-051, REQ-204, REQ-153, REQ-143): The requirements use glossary-avoided terminology. REQ-057 and REQ-051 use “ILS” instead of the preferred “Library Automation System”; REQ-153 uses “library/location” where “Library” should be used for the organizational unit; REQ-204 and REQ-143 use “Non-Cat/non-cat” and “non-category” when referring to Uncataloged material.
- *missing* (REQ-197, C-545): C-545 requires multiple scheduling outputs and multiple output formats for scheduled reports. REQ-197 covers scheduling timing and cancellation but does not require multiple output formats for scheduled reports. The candidate is only partially covered and its output-format content is unrelated to REQ-197.
- *missing* (REQ-154, C-535): C-535 specifically requires snapshot bills history, whereas REQ-154 describes general historical reporting and snapshots of data such as shelving location. The requirement does not explicitly provide historical snapshot reporting for billing state.
- *traceability* (REQ-096, C-322, C-497): C-322 and C-497 require a price-value report by call number or shelving location. REQ-096 covers item value reporting and filtering by status, format, and collection attributes, but does not cover call-number or shelving-location aggregation/filtering. The mapped candidate content is therefore not fully traceable.
- *quality* (REQ-131, C-325, C-326, C-498, C-499): REQ-131 says the system shall generate bibliographic edited and added-by-user reports, but also says those reports were indicated as “not available.” This creates an internally contradictory requirement and does not faithfully represent candidates that explicitly state non-availability.
- *quality* (REQ-132, REQ-200, REQ-151, REQ-018): These requirements use vague, weakly testable terms: “optimal distribution,” “analyze staff productivity and workflow,” “track and verify,” and “efficient”/“timely” cleanup. They lack defined outputs, measures, thresholds, or acceptance conditions.
- *conflict* (REQ-057, REQ-017, REQ-013, REQ-002, REQ-021, REQ-001, REQ-020, REQ-003, REQ-026): REQ-057 states that the system shall not manage acquisitions or cataloging functions, while the listed Cataloging requirements provide substantial item-transfer, purge, deletion, uncataloged-inventory, and status-maintenance utilities. The descriptions attempt to limit the boundary to administrative utilities, but REQ-057 does not state that exception clearly enough.
- *priority* (REQ-028, C-112): REQ-028 is a Could requirement whose rationale says scheduled purging was only questioned and has no agreed contractual requirement. Retaining it as a system shall requirement, even at Could priority, makes the specification stronger than the source evidence supports.
- *quality* (REQ-045): REQ-045 assumes readers need not have common Library terminology defined, while the specification includes a glossary and uses several specialized terms. The assumption is not clearly scoped to common terms versus project-specific terminology and could undermine consistent vocabulary.

## 7. Source documents

| Document | Kind | Date | Candidates extracted |
|---|---|---|---|
| `conversations/conv_pines014_material_volume.eml` | email thread | 2009-04-06 | 19 |
| `conversations/conv_pines015_capacity_interface.eml` | email thread | 2009-04-08 | 18 |
| `conversations/conv_pines016_shelf_space.eml` | email thread | 2009-04-13 | 15 |
| `conversations/conv_pines018_item_transfer.eml` | email thread | 2009-05-11 | 26 |
| `conversations/conv_pines019_020_missing_intransit.eml` | email thread | 2009-04-16 | 16 |
| `conversations/conv_pines021_item_purging.eml` | email thread | 2009-04-21 | 18 |
| `conversations/conv_pines022_deletions.eml` | email thread | 2009-04-24 | 20 |
| `conversations/conv_pines023_patron_characteristics.eml` | email thread | 2009-04-29 | 12 |
| `conversations/conv_pines024_inactive_patrons.eml` | email thread | 2009-05-05 | 27 |
| `early_draft_srs_galecia.txt` | draft requirements specification | 2009-01-27 | 223 |
| `email_financial_reports.eml` | email thread | 2009-07-13 | 20 |
| `email_report_features.eml` | email thread | 2009-07-27 | 28 |
| `email_staff_login.eml` | email thread | 2009-04-09 | 16 |
| `evergreen_reference_2009.txt` | reference documentation | 2009-03-15 | 91 |
| `interview_cataloging_2009-05-08.txt` | interview | 2009-05-08 | 28 |
| `interview_sysadmin_2009-05-10.txt` | interview | 2009-05-10 | 31 |
| `meeting_minutes/meeting_2009-03-15_minutes.txt` | meeting minutes | 2009-03-15 | 24 |
| `meeting_minutes/meeting_2009-07-20_minutes.txt` | meeting minutes | 2009-07-20 | 32 |
| `meeting_tech_subcommittee_2009-06-30.txt` | meeting minutes | 2009-06-30 | 50 |
| `survey_results_2009.txt` | survey results | 2009-04-20 | 38 |
