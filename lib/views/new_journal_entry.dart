import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';
import 'dart:async';
import '../db/database_manager.dart';

class NewJournalEntry extends StatefulWidget {
  static const routeName = 'newJournalEntry';
  const NewJournalEntry({Key? key}) : super(key: key);

  @override
  _NewJournalEntryState createState() => _NewJournalEntryState();
}

class AnimeFields {
  late String title;
  late String review;
  late int rating;
  late String date;

  @override
  String toString() {
    return 'Title: $title, Review: $review, Rating: $rating, Date: $date';
  }
}

class _NewJournalEntryState extends State<NewJournalEntry> {
  final formKey = GlobalKey<FormState>();
  final animeFields = AnimeFields();
  DateTime selectedDate = DateTime.now();

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
        context: context,
        initialDate: selectedDate,
        firstDate: DateTime(1990),
        lastDate: DateTime(2025));
    if (picked != null && picked != selectedDate) {
      setState(() {
        selectedDate = picked;
      });
    }
  }

  Widget buildTitleField() {
    return TextFormField(
        autofocus: true,
        decoration: const InputDecoration(
            labelText: 'Title', border: OutlineInputBorder()),
        validator: (value) {
          if (value == null || value.isEmpty) {
            return 'Title required';
          }
          return null;
        },
        onSaved: (value) {
          animeFields.title = value!;
        });
  }

  Widget buildReviewField() {
    return TextFormField(
        autofocus: true,
        decoration: const InputDecoration(
            labelText: 'Review', border: OutlineInputBorder()),
        validator: (value) {
          if (value == null || value.isEmpty) {
            return 'Review required';
          }
          return null;
        },
        onSaved: (value) {
          animeFields.review = value!;
        });
  }

  Widget buildRatingField() {
    return TextFormField(
        autofocus: true,
        keyboardType: TextInputType.number,
        inputFormatters: <TextInputFormatter>[
          FilteringTextInputFormatter.allow(RegExp(r'[0-9]')),
        ],
        decoration: const InputDecoration(
            labelText: 'Rating', border: OutlineInputBorder()),
        validator: (value) {
          if (value == null || value.isEmpty) {
            return 'Rating required';
          }
          final n = num.tryParse(value);
          if (n == null) {
            return '"$value" is not a valid number';
          } else if (n < 1 || n > 4) {
            return 'Rating must be between 1 and 4';
          }
          return null;
        },
        onSaved: (value) {
          animeFields.rating = int.parse(value!);
        });
  }

  TextEditingController _textEditingController = TextEditingController();
  Widget buildDateField() {
    return TextFormField(
        controller: _textEditingController,
        onTap: () async {
          FocusScope.of(context).requestFocus(FocusNode());
          await _selectDate(context);
          _textEditingController.text =
              DateFormat('yyyy/MM/dd').format(selectedDate);
        },
        decoration: const InputDecoration(
          border: OutlineInputBorder(),
          labelText: 'Date Completed',
          labelStyle: TextStyle(height: 4),
          contentPadding: EdgeInsets.symmetric(horizontal: 10, vertical: 20),
        ),
        validator: (value) {
          if (value == null || value.isEmpty) {
            return 'Date Completed is required';
          }
          return null;
        },
        onSaved: (value) {
          animeFields.date = value!;
        });
  }

  Widget buildSaveButton(BuildContext context) {
    return ElevatedButton(
        onPressed: () async {
          if (formKey.currentState!.validate()) {
            formKey.currentState?.save();
            final databaseManager = DatabaseManager.getInstance();
            databaseManager.saveJournalEntry(dto: animeFields);
            Navigator.of(context).pop();
          }
        },
        child: const Text('Save'));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text("Add new journal entry"),
        ),
        body: Form(
          key: formKey,
          child: Center(
              child: Padding(
            padding: const EdgeInsets.all(10),
            child: Column(children: [
              Flexible(flex:1, child: buildTitleField()),
              Flexible(flex:1, child: buildReviewField()),
              Flexible(flex:1, child: buildRatingField()),
              Flexible(flex:1, child: buildDateField()),
              Flexible(flex:1, child: buildSaveButton(context)),
            ]),
          )),
        ));
  }
}
