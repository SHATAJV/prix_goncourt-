
Purpose
The system allows jurors and a president to vote on book selections through multiple phases, eventually leading to the selection of a final winner. Each phase has different rules regarding the number of books that can be voted on and the number of votes allowed per juror. The president plays a central role in curating the final selection based on the voting results.

Functional Components

Public User:
o	Public users can log in and view the books in a specific selection (e.g., selection 1, 2, or 3) based on their choice.
o	They do not participate in voting but have access to the same book information (e.g., title and author) as other users.

User Roles
o	Jury Members: Jury members can log in to the system, view book selections, and vote on books during specific selection phases. Each jury member has a limited number of votes per phase.
o	President: The president manages the book selection process by adding books to new selection phases and choosing which books progress to the next phase based on jury voting results.
Book Selections
o	Phase 1: Initial Book List: In this phase, a large set of books is made available (e.g., 16 books). No voting is required, as the books are preselected by the president.
o	Phase 2: Jury Voting: Jury members can vote on up to 4 books. After voting, the president selects 8 books based on the highest vote counts.
o	Phase 3: Further Jury Voting: Jury members vote on the 8 books from Phase 2, but this time they can vote for only 2 books. The president selects the top books based on these votes.
o	Phase 4: Final Voting: Jury members vote for 1 book from the final selection, and the president uses these results to determine the final winner.
Voting Mechanics
o	Vote Limits: Each jury member can vote on a specific number of books per selection phase:
	Phase 2: 4 votes maximum per jury member.
	Phase 3: 2 votes maximum per jury member.
	Phase 4: 1 vote per jury member.
o	The system tracks the number of votes cast by each juror, ensuring they do not exceed their allowed votes.
Selection Management
o	The president is responsible for adding books to the selection for each phase and reviewing the voting results.
o	After each jury voting round, the president can view the total votes for each book and select which books progress to the next phase based on these results.
Login and Authentication
o	Each user (jury member or president) must log in with their credentials. Depending on their role, they are presented with different menu options:
	Jury Members: Can view the current book selection and vote.
	President: Can manage the selections by adding books and reviewing vote results.





