import unittest
from pylti1p3.roles import (
    StudentRole,
    TeacherRole,
    StaffRole,
    TeachingAssistantRole,
    DesignerRole,
    ObserverRole,
    TransientRole,
)

MEMBERSHIP = "http://purl.imsglobal.org/vocab/lis/v2/membership#{}"
INSTITUTION = "http://purl.imsglobal.org/vocab/lis/v2/institution/person#{}"
SYSTEM = "http://purl.imsglobal.org/vocab/lis/v2/system/person#{}"
ROLES_CLAIM = "https://purl.imsglobal.org/spec/lti/claim/roles"


def jwt_body(*role_urns):
    return {ROLES_CLAIM: list(role_urns)}


class TestStudentRole(unittest.TestCase):
    def test_context_learner_is_student(self):
        self.assertTrue(StudentRole(jwt_body(MEMBERSHIP.format("Learner"))).check())

    def test_context_member_is_student(self):
        self.assertTrue(StudentRole(jwt_body(MEMBERSHIP.format("Member"))).check())

    def test_institution_student_is_student(self):
        self.assertTrue(StudentRole(jwt_body(INSTITUTION.format("Student"))).check())

    def test_institution_prospective_student_is_student(self):
        self.assertTrue(
            StudentRole(jwt_body(INSTITUTION.format("ProspectiveStudent"))).check()
        )

    def test_teacher_context_role_is_not_student(self):
        self.assertFalse(StudentRole(jwt_body(MEMBERSHIP.format("Instructor"))).check())

    def test_empty_roles_returns_false(self):
        self.assertFalse(StudentRole(jwt_body()).check())


class TestTeacherRole(unittest.TestCase):
    def test_context_instructor_is_teacher(self):
        self.assertTrue(TeacherRole(jwt_body(MEMBERSHIP.format("Instructor"))).check())

    def test_context_administrator_is_teacher(self):
        self.assertTrue(
            TeacherRole(jwt_body(MEMBERSHIP.format("Administrator"))).check()
        )

    def test_student_context_role_is_not_teacher(self):
        self.assertFalse(TeacherRole(jwt_body(MEMBERSHIP.format("Learner"))).check())


class TestStaffRole(unittest.TestCase):
    def test_institution_instructor_is_staff(self):
        self.assertTrue(StaffRole(jwt_body(INSTITUTION.format("Instructor"))).check())

    def test_system_administrator_is_staff(self):
        self.assertTrue(StaffRole(jwt_body(SYSTEM.format("Administrator"))).check())

    def test_institution_faculty_is_staff(self):
        self.assertTrue(StaffRole(jwt_body(INSTITUTION.format("Faculty"))).check())

    def test_student_is_not_staff(self):
        self.assertFalse(StaffRole(jwt_body(MEMBERSHIP.format("Learner"))).check())


class TestContextRolesPrecedence(unittest.TestCase):
    """PR #13 — context roles take priority over institution/system roles."""

    def test_institution_instructor_with_context_learner_is_not_teacher(self):
        # Canvas sends institution Instructor even when the user is a student in this course.
        body = jwt_body(
            INSTITUTION.format("Instructor"),
            MEMBERSHIP.format("Learner"),
        )
        self.assertFalse(TeacherRole(body).check())

    def test_institution_instructor_with_context_learner_is_student(self):
        body = jwt_body(
            INSTITUTION.format("Instructor"),
            MEMBERSHIP.format("Learner"),
        )
        self.assertTrue(StudentRole(body).check())

    def test_without_context_roles_institution_instructor_is_teacher(self):
        # When there are no context roles, institution roles are checked normally.
        body = jwt_body(INSTITUTION.format("Instructor"))
        self.assertFalse(
            TeacherRole(body).check()
        )  # TeacherRole has no institution roles

    def test_staff_institution_without_context_roles(self):
        body = jwt_body(INSTITUTION.format("Instructor"))
        self.assertTrue(StaffRole(body).check())


class TestOtherRoles(unittest.TestCase):
    def test_teaching_assistant(self):
        self.assertTrue(
            TeachingAssistantRole(
                jwt_body(MEMBERSHIP.format("TeachingAssistant"))
            ).check()
        )

    def test_designer(self):
        self.assertTrue(
            DesignerRole(jwt_body(MEMBERSHIP.format("ContentDeveloper"))).check()
        )

    def test_observer(self):
        self.assertTrue(ObserverRole(jwt_body(MEMBERSHIP.format("Mentor"))).check())

    def test_transient(self):
        self.assertTrue(TransientRole(jwt_body(MEMBERSHIP.format("Transient"))).check())

    def test_unknown_role_string_returns_false(self):
        body = jwt_body("urn:some-unknown-role")
        self.assertFalse(StudentRole(body).check())


if __name__ == "__main__":
    unittest.main()
