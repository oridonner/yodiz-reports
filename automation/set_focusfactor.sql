update users set focusfactor = 0.5 where firstname in ('Ben','Ofer','Gil','Yuval');
update users set focusfactor = 0.75 where firstname not in ('Ben','Ofer','Gil','Yuval');