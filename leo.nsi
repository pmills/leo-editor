
;;; This doesn't work.
;;; !addincludedir C:\leo.repo\leo-editor\leo\dist

!include MUI2.nsh
!include nsDialogs.nsh
!include LogicLib.nsh

;##version
!define version         "5.3-final"

; These are *not* Python strings--backslashes are fine.

!define app_icon        "leo\Icons\LeoApp.ico"
!define doc_icon        "leo\Icons\LeoDoc.ico"
; This works, but the icon is too small.
;!define icon            "C:\leo.repo\trunk\leo\Icons\SplashScreen.ico"
!define ext             ".leo"
!define leo_hklm        "SOFTWARE\EKR\Leo"
!define license         "License.txt"
!define name            "Leo"
!define publisher       "Edward K. Ream"
!define site            "http://leoeditor.com/"
!define target_file     "LeoSetup-${version}.exe"
!define uninst_key      "Software\Microsoft\Windows\CurrentVersion\Uninstall\leo"

!include nsi-boilerplate.txt
