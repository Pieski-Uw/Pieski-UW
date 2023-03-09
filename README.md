# InzynieriaOprogramowania

Zapraszam do wpisywania sugestii projektu 

1. Dodatkowy filtr na strony internetowe z ubraniami. Użytkownik tworzy kryterium tzn. wybiera materiały oraz widełki jaki łącznie procent mają one stanowić w składzie. Filtr wyświetla ubrania spełniające kryterium/kryteria.
Wydaje mi się to przydatne, bo wyświetlanie np. swetrów zawierających co najmniej 50% naturalnych materiałów ułatwi zakupy, a przy aktualnie dostępnych opcjach można tylko wyświetlić ubrania mające co najmniej jeden z zaznaczonych materiałów. Nie wiem na ile trudne jest coś takiego do zrobienia.
- brzmi spoko ale targetujemy jakie strony bo rózne pewnie maja różne systemy

2. Aplikacja do dzielenia się paragonami. Robie już ją od dwóch lat chyba ale pomysł brzmi całkiem fajnie (imo ofc). Ma to polegać na możliwości dodawania paragonów i każdy użytkownik w grupie będzie mógł wybrać co jest jego a system automatycznie policzy ile jest kto komu winien. Coś w stylu splitwise ale bardziej zaawansowane. Jakbyśmy robili całość działałoby na django z możliwością rozszerzenia frontendu do reacta. Niewiem czy nie jest to zbyt ambitne ale można o tym pomyśleć też.

3. [pomysł franka] Aplikacja do androida gdzie dla każdego miasta oceniasz je i dodajesz co warto zobaczyć. Całość ma polegać na tym ze użytkownicy dodaja info. (moja opinia (artura) jest taka ze troche tripadvisor ale też można o tym pomyśleć))

4. [Mateusz]  
Zbieranie i tworzenie statystyk na temat adoptowanych zwierząt z np. Schroniska na Paluchu
    - zebranie danych  
    https://napaluchu.waw.pl/zwierzeta/znalazly-dom/  
    fetch strony html,  
    regex, żeby znaleźć linki podstron,  
    regex po podstronach żeby wypełnić sobie baze w SQL   
    testowalne przez przechowanie strony lokalnie i zobaczenie czy parser dobrze działa
    - Analiza danych  
    obliczenie wskaźników ile +/- zwierzę o danych parametrach jest w schronisku  
    (można zrobić na pałę po przedziałach lub zrobić drobną klasyfikację AI)  
    testowalne przez mockowanie jakiś małych danych i sprawdzenie czy jest w +/- przedziale 
    - Prezentacja  
    Prosta stronka gdzie wybierasz parametry zwierzaka (pleć, wiek, masa, rasa)  
    Pokazuje Ci podstawowe dane statystyczne ile podobne spędzały czasu w przeszłości i czy znalazły dom  
    można ambitniej, np jak to się zmieniało w czasie.  
    
    