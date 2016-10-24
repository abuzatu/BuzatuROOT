#include "Body.h"

//constructors
Body::Body() {

}

Body::Body(const std::string& name, double mass, 
	   const Vector3D& x, const Vector3D& v):
  m_name(name),m_mass(mass),m_x(x),m_v(v) {
}  

//destructor
Body::~Body() {

}

//setters

void Body::SetName(const std::string& name) {
  m_name=name;
}

void Body::SetMass(double mass) {
  m_mass=mass;
}

void Body::SetX(const Vector3D& x) {
  m_x=x;
}

void Body::SetV(const Vector3D& v) {
  m_v=v;
}

//getters

std::string Body::GetName() const {
  return m_name;
}

double Body::GetMass() const {
  return m_mass;
}

Vector3D Body::GetX() const {
  return m_x;
}

Vector3D Body::GetV() const {
  return m_v;
}

//others
void Body::Print() {
    std::cout
      <<std::setw(6)<<"Name"
      <<std::setw(12)<<m_name
      <<std::setw(10)<<"Mass"
      <<std::setw(15)<<m_mass
      <<std::setw(10)<<"Position"<<m_x
      <<std::setw(10)<<"Velocity"<<m_v
      <<std::endl;
}

void Body::Evolve(double dt, const Vector3D& a) {
  m_x=m_x+m_v*dt+a*dt*dt*0.5;
  m_v=m_v+a*dt;
}

//these do not belong to do the class, so no need of Body::

bool compare_by_name(const Body& left, const Body& right) {
  return left.GetName()<right.GetName();
}

bool compare_by_mass(const Body& left, const Body& right) {
  return left.GetMass()<right.GetMass();
}

