import 'package:flutter/material.dart';
import 'package:journal/views/journal_entry.dart';
import 'package:journal/views/new_journal_entry.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'views/welcome.dart';

class MyApp extends StatefulWidget {
  final SharedPreferences preferences;
  const MyApp({Key? key, required this.preferences})
      : super(key: key);

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  static const DARK_THEME = 'darkTheme';
  bool get darkTheme => widget.preferences.getBool(DARK_THEME) ?? false;

  var routes = {
    'newEntry': (context) => NewJournalEntry(),
    'journalEntry': (context) => JournalEntry()
  };

  void toggleTheme(bool value) {
    setState(() {
      widget.preferences.setBool(DARK_THEME, !darkTheme);
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      routes: routes,
      title: 'MyAnimeJournal',
      theme: darkTheme ? ThemeData.dark() : ThemeData.light(),
      home: WelcomePage(
          title: 'MyAnimeJournal', darkTheme: darkTheme, toggleTheme: toggleTheme),
    );
  }
}
