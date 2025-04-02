<h3>Opis</h3>
<p>Potrebno je implementirati sistem za upravljanje korisnicima, rolama i permisijama koristeći <strong>SQLAlchemy</strong> u kombinaciji sa <strong>MySQL</strong> ili <strong>PostgreSQL</strong> bazom podataka. Sistem treba omogućiti:</p>
<ul data-spread="false">
<li>
<p>Kreiranje, čitanje, ažuriranje i brisanje (CRUD) korisnika</p>
</li>
<li>
<p>Kreiranje, čitanje, ažuriranje i brisanje (CRUD) rola</p>
</li>
<li>
<p>Kreiranje, čitanje, ažuriranje i brisanje (CRUD) permisija</p>
</li>
<li>
<p>Povezivanje korisnika sa rolama i permisijama</p>
</li>
<li>
<p>Povezivanje rola sa permisijama</p>
</li>
</ul>
<h3>Tehnički zahtevi</h3>
<ol start="1" data-spread="false">
<li>
<p><strong>Baza podataka:</strong> MySQL ili PostgreSQL</p>
</li>
<li>
<p><strong>ORM:</strong> SQLAlchemy</p>
</li>
<li>
<p><strong>Struktura tabela:</strong></p>
<ul data-spread="false">
<li>
<p><code>users</code> (korisnici)</p>
</li>
<li>
<p><code>roles</code> (role)</p>
</li>
<li>
<p><code>permissions</code> (permisije)</p>
</li>
<li>
<p><code>user_roles</code> (tabela za povezivanje korisnika i rola)</p>
</li>
<li>
<p><code>role_permissions</code> (tabela za povezivanje rola i permisija)</p>
</li>
</ul>
</li>
</ol>
<p>Useru je potrebno omoguciti logovanje putem jedne metode i objasniti zasto je bas ta izabrana:</p>
<ul>
<li>Klasična autentikacija</li>
<li>Sessionid</li>
<li>JWT</li>
<li>OAuth 2.0</li>
</ul>
<p>Potrebno je uraditi sto vise jer ocekujem da cete ovo moci raditi danas i sjutra.<br>(Napraviti tako da mozete iskoristiti kasnije za projekat).<br><br></p></div></div>
                                                                            </div>
                                                                    
                                                                    
