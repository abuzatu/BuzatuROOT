#ifndef __Vector3D_h__
#define __Vector3D_h__

#include "TObject.h"

//C++ libraries
#include <math.h> //for sqrt()
#include <iostream> //for cout, endl, ostream

//my libraries

//declarations of functions or classes 
//that are implmented in the .cxx of this folder
class Vector3D
{
  //methods
 public:

  //constructor
  Vector3D();
  Vector3D(double x, double y, double z);
  Vector3D(const Vector3D& v);
  
  //destructor
  ~Vector3D();

  //setters
  void SetX(double x);
  void SetY(double y);
  void SetZ(double z);
  void SetXYZ(double x, double y, double z);

  //getters
  double GetX() const;
  double GetY() const;
  double GetZ() const;
  double GetModule() const;
  
  //overloading streamer operator, so that we can print the content to cout
  //ex: std::cout<<v<<std::endl;
  //a friend function of the class, i.e. it can access private members of the class
  friend std::ostream& operator<<(std::ostream& os, const Vector3D& rhs);

  //overloading the assignment operator
  //ex: Vector3D v1(3.0,4.0,5.0); Vector3D v2=v1;
  //we assign to v2 the value of v1
  //rhs=right hand side
  //Notice that the = operator takes a const-reference to the right hand side of the assignment
  //The reason for this should be obvious, since we don't want to change that value
  //We only want to change what's on the left hand side.
  //Return a reference to the left hand side, which allows to chain and do:
  //Vector3D v(3.0,4.0,5.0);
  //Vector3D v1,v2,v3,v4;
  //v1=v2=v3=v4=v;
  //read more: http://courses.cms.caltech.edu/cs11/material/cpp/donnie/cpp-ops.html
  Vector3D& operator=(const Vector3D& rhs);

  //compound assignement operators are += , -= and *=
  //they are destructive operators because they change the value on the left

  //addition compounds assignment operator +=

  Vector3D& operator+=(const Vector3D& rhs);

  //subtraction compound assignement operator -=
  //ex: Vector3D v1(3,3); Vector3D v2(1,1); v1-=v2; 
  //v1 becomes (2,2), v2 remains (1,1)
  Vector3D& operator-=(const Vector3D& rhs);

  //multiplication with a number assignement operator *=
  //ex: Vector3D v1(3,3); double a=2; v1*=2;
  //v1 becomes (6,6), a remans 2
  Vector3D& operator*=(double rhs);

  //binary arithmetic operators + - *
  //they don't modify either operand, they return a new value from the two arguments
  //it seems complicated, but we can use the already defined compound assignment operators
  //notice the const everywhere
  const Vector3D operator+(const Vector3D& rhs) const;
  const Vector3D operator-(const Vector3D& rhs) const;
  const Vector3D operator*(double rhs) const;
  //but scalar product can exist in 2D as well; there are no compound assignement operators
  double operator*(const Vector3D& rhs) const;
  //the vectorial product can only exist in 3D and we have a 2D vector
  const Vector3D operator^(const Vector3D& rhs) const;

  //the comparison operators == and !=
  bool operator==(const Vector3D& rhs) const;
  bool operator!=(const Vector3D& rhs) const;
  

 private:

  //members
 public:

 private:
  double x_;
  double y_;
  double z_;
  
};

#endif
